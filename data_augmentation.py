import imgaug.augmenters as iaa
import imgaug.parameters as iap
import cv2
import os

number_of_augmentation = 20
number_of_augmented_images = 0


def augment_images(image):
    global number_of_augmentation
    augmented_face_list = []

    # Implementing Brightness, Contrast and Saturation augmentation on the image dataset
    seq = iaa.Sequential(
        [
            # Brightness augmentation
            iaa.OneOf(
                [
                    iaa.WithBrightnessChannels(iaa.Multiply(0.2),
                                               from_colorspace=iaa.CSPACE_RGB,
                                               to_colorspace=iaa.CSPACE_HSV),
                    iaa.WithBrightnessChannels(iaa.Multiply(1.2),
                                               from_colorspace=iaa.CSPACE_RGB,
                                               to_colorspace=iaa.CSPACE_HSV)
                ]
            ),

            # Contrast augmentation
            iaa.OneOf(
                [
                    iaa.CLAHE(clip_limit=(1, 10),
                              tile_grid_size_px=iap.Discretize(iap.Normal(loc=7, scale=2)),
                              tile_grid_size_px_min=3,
                              from_colorspace=iaa.CLAHE.RGB,
                              to_colorspace=iaa.CLAHE.HSV),
                    iaa.CLAHE(clip_limit=(10, 20),
                              tile_grid_size_px=iap.Discretize(iap.Normal(loc=7, scale=2)),
                              tile_grid_size_px_min=3,
                              from_colorspace=iaa.CLAHE.RGB,
                              to_colorspace=iaa.CLAHE.HSV)
                ]
            ),

            # Saturation augmentation
            iaa.OneOf(
                [
                    iaa.MultiplySaturation(1.2,
                                           from_colorspace=iaa.CSPACE_RGB),
                    iaa.MultiplySaturation(0.2,
                                           from_colorspace=iaa.CSPACE_RGB)
                ]
            ),

            # Zoom Augmentation
            iaa.OneOf(
                [
                    iaa.Affine(scale=0.5),
                    iaa.Affine(scale=1.2)
                ]
            )
        ]
    )

    for image_number in range(number_of_augmentation):
        aug_image = seq.augment_image(image=image)
        augmented_face_list.append(aug_image)

    return augmented_face_list


def save_augmented_images(image_list, path, image_name):
    global number_of_augmented_images

    for img in image_list:
        number_of_augmented_images += 1
        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imwrite(os.path.join(path, f'{number_of_augmented_images} - {image_name}.jpg'), image_rgb)


def augmenting_images_from_dataset(dataset, augmented_dataset):
    global number_of_augmented_images

    for class_name in os.listdir(dataset):
        image_class_path = os.path.join(dataset, class_name)

        number_of_augmented_images = 0
        augmenting_images_from_class(class_name, image_class_path, augmented_dataset)


def augmenting_images_from_class(class_name, class_path, augmented_class_path):

    global number_of_augmented_images

    augmented_class_path = os.path.join(augmented_class_path, class_name)

    if os.path.isdir(augmented_class_path) is False:
        os.mkdir(augmented_class_path)

    for (i, image_path) in enumerate(os.listdir(class_path)):
        image_path = os.path.join(class_path, image_path)
        # augmented_image_path = os.path.join(augmented_class_path, frame_1'{class_name} - {i + 1}.jpg')

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        face_list = augment_images(image)

        save_augmented_images(face_list, augmented_class_path, class_name)

    print(f"[INFO] Total faces augmented from {class_name} class: {number_of_augmented_images}")


if __name__ == "__main__":
    Dataset = "Aligned Dataset"
    augmented_dataset_path = "Augmented Dataset"
    augmenting_images_from_dataset(Dataset, augmented_dataset_path)
    # augmenting_images_from_class("Saif", "Aligned Dataset/Saif", augmented_dataset_path)
