import PIL.Image
import torch
from diffusers import StableDiffusionInpaintPipeline

from src.create_prompt import create_prompt_from_news
from src.outpainting_config import OutPaintingConfig
from src.utils import save_image, read_image_batched, save_image_batched
from src.aesthetic_predictor import AestheticPredictor


class Outpainting:
    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state
        if not self._shared_state:
            self.outpainting_config = OutPaintingConfig()
            self.aesthetic_predictor = AestheticPredictor()

            # init model/pipe
            model = self.outpainting_config.get_config("outpainting", "model") or "runwayml/stable-diffusion-inpainting"
            self.pipe = StableDiffusionInpaintPipeline.from_pretrained(
                model,
                revision="fp16",
                torch_dtype=torch.float16
            )
            self.pipe.to("cuda")
        

    def generate_image(self):
        # load params
        default_prompt = self.outpainting_config.get_config("outpainting", "positive_prompt")
        prompt = create_prompt_from_news() + ', ' + default_prompt
        negative_prompt = self.outpainting_config.get_config("outpainting", "negative_prompt")
        guidance_scale = self.outpainting_config.get_config_float("outpainting", "guidance_scale") or 7.5
        num_inference_steps = self.outpainting_config.get_config_int("outpainting", "num_inference_steps") or 10
        height = self.outpainting_config.get_config_int("outpainting", "height") or 512
        width = self.outpainting_config.get_config_int("outpainting", "width") or 512

        # load image
        init_image = read_image_batched("outpainting", "image")
        first_image = False
        if init_image is None:
            init_image = PIL.Image.new("RGB", (width, height), (0, 0, 0))
            first_image = True

        # set params
        output_height = init_image.height
        output_width = init_image.width + (width if not first_image else 0)

        # create working image
        working_image = PIL.Image.new(init_image.mode,
                                    (init_image.width + (width if not first_image else 0), init_image.height), (0, 0, 0))
        working_image.paste(init_image, (0, 0, init_image.width, init_image.height))

        # create mask image
        mask_image = PIL.Image.new("RGB", (init_image.width + (width if not first_image else 0), init_image.height),
                                (0, 0, 0))
        mask_image.paste((255, 255, 255), (
            init_image.width if not first_image else 0, 0, init_image.width + (width if not first_image else 0),
            init_image.height))

        quality = 0
        quality_threshold = self.outpainting_config.get_config_int("outpainting", "quality_threshold")
        while quality < quality_threshold:
            # generate image
            generated_image = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                image=working_image,
                mask_image=mask_image,
                guidance_scale=guidance_scale,
                num_inference_steps=num_inference_steps,
                height=output_height,
                width=output_width,
            ).images[0]

            # check quality
            quality = self.aesthetic_predictor.eval_image(generated_image)
        else:
            if not first_image:
                cropped_image = generated_image.crop((width, 0, width * 2, height))
                save_image_batched(cropped_image, "outpainting", "image")
            else:
                save_image(generated_image, "outpainting", "0001_image")
