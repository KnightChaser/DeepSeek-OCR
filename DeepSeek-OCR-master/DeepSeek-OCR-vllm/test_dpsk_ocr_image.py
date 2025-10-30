# test_dpsk_ocr_image.py
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor
from PIL import Image, ImageOps
import os
import re
import ast

# Matches only image / image_caption ref+det blocks (keep name as requested)
_IMG_TAG = re.compile(
    r"<\|ref\|\>(image|image_caption)<\|/ref\|\><\|det\|\>(\[\[.*?\]\])<\|/det\|\>",
    re.DOTALL,
)

# Strip everything else: text, sub_title, title, etc.
_NON_IMG_TAG = re.compile(
    r"<\|ref\|\>(?!image|image_caption)[^<]+<\|/ref\|\><\|det\|\>\[\[.*?\]\]\<\|/det\|\>",
    re.DOTALL,
)

def _scale_box(box, W, H, pad=2):
    x1, y1, x2, y2 = map(float, box)
    # DeepSeek coords are normalized [0..999]; scale back to pixels
    x1 = int(round(x1 / 999.0 * W))
    y1 = int(round(y1 / 999.0 * H))
    x2 = int(round(x2 / 999.0 * W))
    y2 = int(round(y2 / 999.0 * H))
    # normalize ordering
    if x2 < x1: x1, x2 = x2, x1
    if y2 < y1: y1, y2 = y2, y1
    # optional padding + clamp
    x1 = max(0, x1 - pad); y1 = max(0, y1 - pad)
    x2 = min(W, x2 + pad); y2 = min(H, y2 + pad)
    return (x1, y1, x2, y2)

def rewrite_md_with_embeds(text_output: str, image: Image.Image, output_dir: str, base_img_name: str):
    os.makedirs(output_dir, exist_ok=True)
    W, H = image.size
    pieces = []
    last = 0
    img_counter = 1

    for m in _IMG_TAG.finditer(text_output):
        pieces.append(text_output[last:m.start()])

        label = m.group(1).strip()       # "image" or "image_caption"
        boxes = ast.literal_eval(m.group(2))
        if boxes and isinstance(boxes[0], (int, float)):
            boxes = [boxes]  # normalize single-box to list

        if label == "image":
            md_snips = []
            for b in boxes:
                x1, y1, x2, y2 = _scale_box(b, W, H, pad=2)
                if x2 <= x1 or y2 <= y1:
                    continue
                crop = image.crop((x1, y1, x2, y2))
                crop_name = f"{base_img_name}_img{img_counter}.png"
                crop.save(os.path.join(output_dir, crop_name))
                md_snips.append(f"![Figure {img_counter}]({crop_name})")
                img_counter += 1
            pieces.append("\n".join(md_snips) + "\n")
        else:
            # image_caption bbox → drop (caption text is already in plain text)
            pass

        last = m.end()

    pieces.append(text_output[last:])
    new_md = "".join(pieces)

    # Drop any remaining non-image ref/det blocks (text, sub_title, etc.)
    new_md = _NON_IMG_TAG.sub("", new_md)

    with open(os.path.join(output_dir, f"{base_img_name}.md"), "w", encoding="utf-8") as f:
        f.write(new_md)
    print(f"[OK] Rewrote markdown with embedded images to {output_dir}")

def process_single_image(image_path: str,
                         output_md_path: str,
                         model_name: str = "deepseek-ai/DeepSeek-OCR"):
    """
    Processes a single image to extract text and convert it to Markdown format.
    """
    # EXIF-aware load to keep orientation consistent with model preproc
    image = ImageOps.exif_transpose(Image.open(image_path)).convert("RGB")

    # Prepare model instance
    llm = LLM(
        model=model_name,
        enable_prefix_caching=False,
        mm_processor_cache_gb=0,
        logits_processors=[NGramPerReqLogitsProcessor],
        gpu_memory_utilization=0.7
    )

    # Construct prompt
    prompt = "<image>\n<|grounding|>Convert the document to markdown."

    # Prepare single-request input
    model_input = {
        "prompt": prompt,
        "multi_modal_data": {"image": image}
    }

    # Define sampling parameters
    sampling_param = SamplingParams(
        temperature=0.0,
        max_tokens=8192,
        # ngram logit processor arguments
        extra_args=dict(
            ngram_size=30,
            window_size=90,
            whitelist_token_ids={128821, 128822},  # <td>, </td>
        ),
        skip_special_tokens=False,
    )

    # Generate output
    outputs = llm.generate(model_input, sampling_param)  # type: ignore

    print(f"[OK] Generated output for {image_path}")
    for output in outputs:
        print(f"[MODEL OUTPUT] {output.outputs[0].text}")

    # Extract text result
    text_output = outputs[0].outputs[0].text

    # Write raw Markdown (optional; helps debugging)
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(text_output)

    # Rewrite markdown to handle embedded images and drop non-image ref/det
    base_img_name = os.path.splitext(os.path.basename(image_path))[0]
    output_dir = os.path.splitext(output_md_path)[0] + "_assets"
    rewrite_md_with_embeds(text_output, image, output_dir, base_img_name)

    print(f"[OK] Processed {image_path} --> {output_md_path}")
    return text_output

if __name__ == "__main__":
    img_path = "./test_images/test_document_4.png"

    out_md_file_dir = "./output"
    out_md_file_name = "./test_document_4.md"
    os.makedirs(out_md_file_dir, exist_ok=True)
    out_md = os.path.join(out_md_file_dir, out_md_file_name)

    process_single_image(img_path, out_md)


