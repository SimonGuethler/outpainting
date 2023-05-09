import PIL.Image
import torch
from diffusers import StableDiffusionInpaintPipeline

from src.create_prompt import create_prompt_from_news
from src.utils import save_image, read_image_batched, save_image_batched


def outpainting():
    prompt = create_prompt_from_news()
    negative_prompt = ""
    model = "runwayml/stable-diffusion-inpainting"
    width = 512
    height = 512
    init_image = read_image_batched("outpainting", "image")

    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model,
        revision="fp16",
        torch_dtype=torch.float16
    )
    pipe.to("cuda")
    # pipe.enable_attention_slicing()

    first_image = False

    if init_image is None:
        init_image = PIL.Image.new("RGB", (width, height), (0, 0, 0))
        first_image = True

    print(f'Image: {init_image.size}')

    working_image = PIL.Image.new(init_image.mode,
                                  (init_image.width + (width if not first_image else 0), init_image.height), (0, 0, 0))
    working_image.paste(init_image, (0, 0, init_image.width, init_image.height))

    print(f'Working image: {working_image.size}')

    mask_image = PIL.Image.new("RGB", (init_image.width + (width if not first_image else 0), init_image.height),
                               (0, 0, 0))
    mask_image.paste((255, 255, 255), (
        init_image.width if not first_image else 0, 0, init_image.width + (width if not first_image else 0),
        init_image.height))

    print(f'Mask image: {mask_image.size}')

    output_height = init_image.height
    output_width = init_image.width + (width if not first_image else 0)

    generated_image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        image=working_image,
        mask_image=mask_image,
        guidance_scale=7.5,
        num_inference_steps=10,
        height=output_height,
        width=output_width,
    ).images[0]
    
    if not first_image:
        cropped_image = generated_image.crop((width, 0, width*2, height))
        save_image_batched(cropped_image, "outpainting", "image")
    else:
        save_image(generated_image, "outpainting", "0001_image")
outpainting()