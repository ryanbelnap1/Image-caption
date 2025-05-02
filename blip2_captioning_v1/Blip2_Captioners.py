import gradio as gr
from PIL import Image
import os
import time
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import torch
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Gradio app for captioning images")
    parser.add_argument("--share", action="store_true", help="Launch app with Gradio share link")
    return parser.parse_args()

class ModelLoader:
    def __init__(self):
        self.model = None
        self.processor = None
        self.selected_model = None
        self.load_in_8bit = False
        self.load_in_4bit = False
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
    
    def load_model(self, selected_model, load_in_8bit, load_in_4bit):
        if self.selected_model != selected_model or self.load_in_8bit != load_in_8bit or self.load_in_4bit != load_in_4bit or self.model is None:
            if self.model is not None:
                del self.model
                torch.cuda.empty_cache()
            self.processor = Blip2Processor.from_pretrained(selected_model)
            if load_in_4bit:
                load_in_8bit = False  # Prioritize 4-bit over 8-bit if both are selected
            self.model = Blip2ForConditionalGeneration.from_pretrained(selected_model, torch_dtype=torch.float16, load_in_8bit=load_in_8bit,load_in_4bit=load_in_4bit, device_map="cuda:0")
            if not load_in_4bit and not load_in_8bit:  # Fixed logical operation for Python
                self.model.to(self.device)
            self.selected_model = selected_model
            self.load_in_8bit = load_in_8bit
            self.load_in_4bit = load_in_4bit
    
    def generate_caption(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            inputs = self.processor(images=image, return_tensors="pt").to(self.device, torch.float16)
            generated_ids = self.model.generate(**inputs, max_new_tokens=75)
            generated_text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
            
            if torch.cuda.is_available():
                        torch.cuda.empty_cache()
            return generated_text, "Success"
        except Exception as e:
            return "", f"Failed to process image {image_path}. Error: {e}"

model_loader = ModelLoader()

def batch_process(folder_path, selected_model, load_in_8bit, load_in_4bit):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    total_images = len(image_files)
    processed_info = []

    model_loader.load_model(selected_model, load_in_8bit, load_in_4bit)
    
    start_time = time.time()
    for idx, image_file in enumerate(image_files, start=1):
        image_path = os.path.join(folder_path, image_file)
        caption, status = model_loader.generate_caption(image_path)
        elapsed_time = time.time() - start_time
        speed = elapsed_time / idx
        estimated_total_time = speed * total_images
        estimated_remaining_time = estimated_total_time - elapsed_time
        
        # Generate the path for the .txt file
        text_file_path = os.path.splitext(image_path)[0] + '.txt'
        
        # Write the caption to a .txt file in UTF-8 encoding, overwriting existing file
        with open(text_file_path, 'w', encoding='utf-8') as text_file:
            text_file.write(caption)
        
        print(f"Image {idx}/{total_images}: {status}, Speed: {speed:.2f} s/image, ETA: {estimated_remaining_time:.2f} s")
        processed_info.append(f"Image {idx}/{total_images}: {caption}, Speed: {speed:.2f} s/image, Estimated Time Remaining: {estimated_remaining_time:.2f} s")
    
    return "\n".join(processed_info)

def single_image_process(image, selected_model, load_in_8bit, load_in_4bit):
    model_loader.load_model(selected_model, load_in_8bit, load_in_4bit)
    caption, status = model_loader.generate_caption(image)
    vram_usage = measure_vram_usage()
    print(caption)
    return caption, vram_usage
	
def measure_vram_usage():
    if torch.cuda.is_available():
        current_vram = torch.cuda.memory_allocated() / (1024 ** 3)  # Convert bytes to GB
        peak_vram = torch.cuda.max_memory_allocated() / (1024 ** 3)  # Convert bytes to GB
        torch.cuda.reset_peak_memory_stats()  # Reset peak memory stats for next measurement
    else:
        current_vram, peak_vram = 0, 0  # Set to 0 if CUDA is not available
    return f"Current VRAM: {current_vram:.2f} GB, Peak VRAM: {peak_vram:.2f} GB"
	

def update_vram_info(model, load_in_8bit, load_in_4bit):
    if load_in_4bit:  # Adjust VRAM usage for 4-bit loading
        vram_usage = {
            "Salesforce/blip2-opt-6.7b": "~6 GB VRAM",
            "Salesforce/blip2-flan-t5-xxl": "~15 GB VRAM",
            "Salesforce/blip2-opt-6.7b-coco": "~6 GB VRAM"
        }
    else:
        vram_usage = {
            "Salesforce/blip2-opt-6.7b": "~9 GB VRAM" if load_in_8bit else "~16 GB VRAM",
            "Salesforce/blip2-flan-t5-xxl": "~19.5 GB VRAM" if load_in_8bit else "~29.5 GB VRAM",
            "Salesforce/blip2-opt-6.7b-coco": "~9 GB VRAM" if load_in_8bit else "~16 GB VRAM"
        }
    return vram_usage[model]

# Define Gradio interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("### Blip 2 Models Batch Image Captioning App")
        
        with gr.Row():
            with gr.Column(scale=1):

                model_choice = gr.Dropdown(label="Select Model", choices=["Salesforce/blip2-opt-6.7b", "Salesforce/blip2-flan-t5-xxl", "Salesforce/blip2-opt-6.7b-coco"], value="Salesforce/blip2-opt-6.7b")
                load_in_8bit_checkbox = gr.Checkbox(label="Load in 8 bit precision")
                load_in_4bit_checkbox = gr.Checkbox(label="Load in 4 bit precision")
                vram_info = gr.Textbox(label="Approximate VRAM Usage", value="~15 GB VRAM")  # Default model VRAM usage
                single_output = gr.Textbox(label="Single Image Captioning Results")
                single_btn = gr.Button("Caption Single Image")	
                folder_path = gr.Text(label="Folder Path for Batch Processing")	
                				
            with gr.Column(scale=1):
                image_file = gr.Image(label="Upload Single Image", type="filepath", height=500)
                vram_usage_output = gr.Textbox()
        
        with gr.Row():
            
            batch_btn = gr.Button("Batch Process Images")
            batch_output = gr.Textbox(label="Batch Processing Status", lines=5)
        
        def update_vram(model, load_in_8bit, load_in_4bit):
            return update_vram_info(model, load_in_8bit, load_in_4bit)
        
        model_choice.change(lambda x, y, z: update_vram(x, y, z), inputs=[model_choice, load_in_8bit_checkbox, load_in_4bit_checkbox], outputs=[vram_info])
        load_in_8bit_checkbox.change(lambda x, y, z: update_vram(x, y, z), inputs=[model_choice, load_in_8bit_checkbox, load_in_4bit_checkbox], outputs=[vram_info])
        load_in_4bit_checkbox.change(lambda x, y, z: update_vram(x, y, z), inputs=[model_choice, load_in_8bit_checkbox, load_in_4bit_checkbox], outputs=[vram_info])
        
        single_btn.click(fn=single_image_process, inputs=[image_file, model_choice, load_in_8bit_checkbox, load_in_4bit_checkbox], outputs=[single_output,vram_usage_output])
        batch_btn.click(fn=batch_process, inputs=[folder_path, model_choice, load_in_8bit_checkbox, load_in_4bit_checkbox], outputs=[batch_output])

    return demo

if __name__ == "__main__":
    args = parse_args()
    demo = create_interface()
    demo.queue().launch(share=args.share, inbrowser=True)
