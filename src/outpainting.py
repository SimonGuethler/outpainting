import PIL.Image
import torch
from diffusers import StableDiffusionInpaintPipeline, StableDiffusionPipeline

from src.aesthetic_predictor import AestheticPredictor
from src.create_prompt import create_prompt_from_news
from src.outpainting_config import OutPaintingConfig
from src.utils import save_image, read_image_batched, save_image_batched, convert_img_to_webp, write_to_file


class Outpainting:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.outpainting_config = OutPaintingConfig()
            self.aesthetic_predictor = AestheticPredictor()

            # init inpainting model/pipe
            inpainting_model = self.outpainting_config.get_config("outpainting", "inpainting_model") or "runwayml/stable-diffusion-inpainting"
            self.inpainting_pipe = StableDiffusionInpaintPipeline.from_pretrained(
                inpainting_model,
                revision="fp16",
                torch_dtype=torch.float16
            )
            self.inpainting_pipe.to("cuda")

            # init main model/pipe
            main_model = self.outpainting_config.get_config("outpainting", "main_model") or "runwayml/stable-diffusion-v1-5"
            self.main_pipe = StableDiffusionPipeline.from_pretrained(
                main_model,
                revision="fp16",
                torch_dtype=torch.float16
            )
            self.main_pipe.to("cuda")


    def generate_image(self):
        # load params
        default_prompt = self.outpainting_config.get_config("outpainting", "positive_prompt")
        news_prompt = create_prompt_from_news()
        negative_prompt = self.outpainting_config.get_config("outpainting", "negative_prompt")
        pre_prompt = self.outpainting_config.get_config("outpainting", "pre_prompt")
        guidance_scale = self.outpainting_config.get_config_float("outpainting", "guidance_scale") or 7.5
        guidance_scale_trans = self.outpainting_config.get_config_float("outpainting", "guidance_scale_trans") or 7.5
        num_inference_steps = self.outpainting_config.get_config_int("outpainting", "num_inference_steps") or 10
        height = self.outpainting_config.get_config_int("outpainting", "height") or 512
        width = self.outpainting_config.get_config_int("outpainting", "width") or 512

        # generate main image
        quality = 0
        quality_threshold = self.outpainting_config.get_config_float("outpainting", "quality_threshold")
        quality_step = self.outpainting_config.get_config_float("outpainting", "quality_step")
        generated_image = PIL.Image.new("RGB", (width, height), (0, 0, 0))
        while quality < quality_threshold:
            # generate image
            generated_image = self.main_pipe(
                prompt=pre_prompt + ' ' + news_prompt + ', ' + default_prompt,
                negative_prompt=negative_prompt,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                height=height,
                width=width,
            ).images[0]

            # check quality
            quality = self.aesthetic_predictor.eval_image(generated_image)
            quality_threshold -= quality_step

        # generate transition
        init_image = read_image_batched("outpainting", "image")
        if init_image is not None:
            # load image
            if init_image is None:
                init_image = PIL.Image.new("RGB", (width, height), (0, 0, 0))

            # set params
            output_height = init_image.height
            output_width = init_image.width + 2 * width

            # create working image
            working_image = PIL.Image.new(init_image.mode,
                                        (init_image.width + 2 * width, init_image.height),
                                        (0, 0, 0))
            working_image.paste(init_image, (0, 0, init_image.width, init_image.height))    # left image
            working_image.paste(generated_image, (init_image.width + width, 0, init_image.width + width + generated_image.width, generated_image.height))    # right image

            # create mask image
            mask_image = PIL.Image.new("RGB", (init_image.width + 2 * width, init_image.height),
                                    (0, 0, 0))
            mask_image.paste((255, 255, 255), (
                init_image.width, 0, init_image.width + width,
                init_image.height))

            quality = 0
            quality_threshold = self.outpainting_config.get_config_float("outpainting", "quality_threshold")
            quality_step = self.outpainting_config.get_config_float("outpainting", "quality_step")
            generated_transition = PIL.Image.new("RGB", (width, height), (0, 0, 0))
            while quality < quality_threshold:
                # generate image
                generated_transition = self.inpainting_pipe(
                    prompt=default_prompt,
                    negative_prompt=negative_prompt,
                    image=working_image,
                    mask_image=mask_image,
                    guidance_scale=guidance_scale_trans,
                    num_inference_steps=num_inference_steps,
                    height=output_height,
                    width=output_width,
                ).images[0]

                # check quality
                quality = self.aesthetic_predictor.eval_image(generated_transition)
                quality_threshold -= quality_step
            else:
                cropped_image = generated_transition.crop((width, 0, width * 2, height))
                filename = save_image_batched(cropped_image, "outpainting", "image")
                write_to_file('outpainting', 'prompts.txt', '-\n', append=True)
                convert_img_to_webp(f"outpainting/{filename}")

        # save main image
        if init_image is not None:
            filename = save_image_batched(generated_image, "outpainting", "image")
            write_to_file('outpainting', 'prompts.txt', f'{news_prompt}\n', append=True)
            convert_img_to_webp(f"outpainting/{filename}")
        else:
            filename = save_image(generated_image, "outpainting", "0001_image")
            write_to_file('outpainting', 'prompts.txt', f'{news_prompt}\n', append=True)
            convert_img_to_webp(f"outpainting/{filename}")
