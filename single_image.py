from diffusers import DiffusionPipeline

from utils import save_image

model = "runwayml/stable-diffusion-v1-5"
pipe = DiffusionPipeline.from_pretrained(model)
pipe.to("cuda")

prompt = "An image of a squirrel in Picasso style"
negative_prompt = ''

for i in range(10):
    print(f"Generating image: {i + 1} / 10")
    image = pipe(
        prompt,
        negative_prompt=negative_prompt,
        guidance_scale=7.5,
        num_inference_steps=25,
        num_images_per_prompt=1,
        height=512,
        width=512
    ).images[0]

    save_image(image, "images", prompt)
