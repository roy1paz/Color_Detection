import os
import cv2 as cv
import numpy as np
from tqdm import tqdm
import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt


def color_detection(img_path, color_range):
    img = cv.imread(img_path)
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Define the lower and upper bounds of the color range
    lower_bound = np.array(color_range[0])
    upper_bound = np.array(color_range[1])

    # Create a mask for the specified color range
    mask = cv.inRange(img_hsv, lower_bound, upper_bound)

    # Bitwise AND to extract the color region
    color_region = cv.bitwise_and(img, img, mask=mask)

    # Combine the original image and the color region
    highlighted_image = cv.addWeighted(img, 1, color_region, 0.8, 0)

    # Calculate the percentage coverage and round it.
    total_pixels = np.prod(img.shape[:2])
    colored_pixels = np.sum(mask > 0)
    coverage_percentage = np.round((colored_pixels / total_pixels) * 100, 3)

    # Save the original image, color region, mask image and Highlighted Image
    fig, axes = plt.subplots(1, 4, figsize=(15, 5))
    plt.subplots_adjust(wspace=0.05)
    plt.suptitle(f"Percentage coverage: {coverage_percentage}%", y=0.1)

    axes[0].imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    axes[0].set_title('Original Image')
    axes[0].set_xticks([]), axes[0].set_yticks([])

    axes[1].imshow(cv.cvtColor(mask, cv.COLOR_BGR2RGB))
    axes[1].set_title('Mask Image')
    axes[1].set_xticks([]), axes[2].set_yticks([])

    axes[2].imshow(cv.cvtColor(color_region, cv.COLOR_BGR2RGB))
    axes[2].set_title('Colored Mask')
    axes[2].set_xticks([]), axes[1].set_yticks([])

    axes[3].imshow(cv.cvtColor(highlighted_image, cv.COLOR_BGR2RGB))
    axes[3].set_title('Highlighted Image')
    axes[3].set_xticks([]), axes[3].set_yticks([])

    path_to_save = "results/" + img_path[6:]
    plt.savefig(path_to_save)
    plt.close()


if __name__ == "__main__":
    # HSV example - red color
    min_hue, min_saturation, min_value = 0, 100, 100
    max_hue, max_saturation, max_value = 10, 255, 255

    HSV_range = [
        [min_hue, min_saturation, min_value],  # Lower bound
        [max_hue, max_saturation, max_value]]  # Upper bound

    # create results directory if not exists
    if not os.path.exists("results"):
        os.mkdir("results")

    # iterate over images test path
    for dirname, _, filenames in os.walk('images'):
        for filename in tqdm(filenames):
            path = os.path.join(dirname, filename)
            color_detection(path, HSV_range)
