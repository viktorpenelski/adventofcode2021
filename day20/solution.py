from copy import deepcopy
from typing import List


def parse_inputs():
    def _map_to_binary_list(line: str) -> List[int]:
        return [(1 if x == '#' else 0) for x in line.strip()]

    with open('in.txt') as f:
        lines = f.readlines()
        image_enhancement_algo = _map_to_binary_list(lines[0])
        img = []
        for line_idx in range(2, len(lines)):
            img.append(_map_to_binary_list(lines[line_idx]))

        return image_enhancement_algo, img


def pad_header_and_footer(img: List[List[int]], out_px: int) -> List[List[int]]:
    img = deepcopy(img)
    for row in img:
        row.insert(0, out_px)
        row.append(out_px)
    padding_len = len(img[0])
    img.insert(0, [out_px] * padding_len)
    img.append([out_px] * padding_len)
    return img


def get_3_by_3_binary(row_idx: int, col_idx: int, img: List[List[int]], out_px: int) -> str:
    binary = ''
    for r_idx in range(row_idx - 1, row_idx + 2):
        for c_idx in range(col_idx - 1, col_idx + 2):
            if r_idx < 0 or r_idx >= len(img) or c_idx < 0 or c_idx >= len(img[r_idx]):
                binary += str(out_px)
            else:
                binary += str(img[r_idx][c_idx])
    return binary


def parse_img(img: List[List[int]], img_enhancer: List[int], out_px: int) -> List[List[int]]:
    img_out = deepcopy(img)
    for r in range(len(img_out)):
        for c in range(len(img_out[r])):
            enh_idx = int(get_3_by_3_binary(r, c, img, out_px), 2)
            img_out[r][c] = img_enhancer[enh_idx]
    return img_out


img_enh, input_img = parse_inputs()
pixel_outside = 0
image = pad_header_and_footer(input_img, pixel_outside)
for i in range(50):
    if i == 2:
        print(f'2 iterations: {sum(sum(line) for line in image)}')
    image = parse_img(image, img_enh, pixel_outside)
    pixel_outside = img_enh[0] if pixel_outside == 0 else img_enh[511]
    image = pad_header_and_footer(image, pixel_outside)

print(f'50 iterations: {sum(sum(line) for line in image)}')
