import os
import shutil
import xml.etree.ElementTree as ET
from urllib.parse import unquote, urlparse

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import dir_exists, file_exists, get_file_ext, get_file_name
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/Makerere University Beans Image/dataverse_files (1)"
    images_ext = ".jpg"
    bboxes_ext = ".xml"
    ds_name = "ds"
    batch_size = 30

    def create_ann(image_path):
        labels = []
        tags = []

        subfolder_tag = sly.Tag(subfolder_tag_meta)
        tags.append(subfolder_tag)

        ann_path = image_path.replace(images_ext, bboxes_ext)

        if file_exists(ann_path):
            tree = ET.parse(ann_path)
            root = tree.getroot()

            image_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = image_np.shape[0]
            img_wight = image_np.shape[1]

            variety_value = root.find(".//variety").text
            variety = sly.Tag(variety_meta, value=variety_value)
            age_value = int(root.find(".//age").text)
            age = sly.Tag(age_meta, value=age_value)
            district_value = root.find(".//district").text
            district = sly.Tag(district_meta, value=district_value)
            datetime_value = root.find(".//datetime").text
            datetime = sly.Tag(datetime_meta, value=datetime_value)
            subcounty_value = root.find(".//subcounty").text
            subcounty = sly.Tag(subcounty_meta, value=subcounty_value)
            symptoms_value = root.find(".//hasOtherSymptoms").text
            if symptoms_value != "False":
                symptoms = sly.Tag(symptoms_meta)
                tags.append(symptoms)

            tags.extend([variety, age, district, datetime, subcounty])

            objects = root.findall(".//object")
            for curr_obj in objects:
                name = curr_obj.find(".//name").text
                obj_class = name_to_class.get(name)
                curr_coord = curr_obj.find(".//bndbox")
                left = int(curr_coord[0].text)
                top = int(curr_coord[1].text)
                right = int(curr_coord[2].text)
                bottom = int(curr_coord[3].text)

                rect = sly.Rectangle(left=left, top=top, right=right, bottom=bottom)
                label = sly.Label(rect, obj_class)
                labels.append(label)

        else:
            image_np = sly.imaging.image.read(image_path)[:, :, 0]
            img_height = image_np.shape[0]
            img_wight = image_np.shape[1]

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    br = sly.ObjClass("bean rust", sly.Rectangle)
    als = sly.ObjClass("angular leaf spot", sly.Rectangle)

    name_to_class = {"Bean Rust": br, "ALS": als}

    healthy_meta = sly.TagMeta("healthy", sly.TagValueType.NONE)
    als_meta = sly.TagMeta("als", sly.TagValueType.NONE)
    bean_rust_meta = sly.TagMeta("bean rust", sly.TagValueType.NONE)

    subfolder_to_tag = {
        "healthy_1": healthy_meta,
        "healthy_2": healthy_meta,
        "als_1": als_meta,
        "als_2": als_meta,
        "bean_rust_1": bean_rust_meta,
        "bean_rust_2": bean_rust_meta,
    }

    variety_meta = sly.TagMeta("variety", sly.TagValueType.ANY_STRING)
    age_meta = sly.TagMeta("age", sly.TagValueType.ANY_NUMBER)
    district_meta = sly.TagMeta("district", sly.TagValueType.ANY_STRING)
    datetime_meta = sly.TagMeta("datetime", sly.TagValueType.ANY_STRING)
    subcounty_meta = sly.TagMeta("subcounty", sly.TagValueType.ANY_STRING)
    symptoms_meta = sly.TagMeta("has other symptoms", sly.TagValueType.NONE)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    meta = sly.ProjectMeta(
        obj_classes=[br, als],
        tag_metas=[
            variety_meta,
            age_meta,
            district_meta,
            datetime_meta,
            subcounty_meta,
            symptoms_meta,
            healthy_meta,
            als_meta,
            bean_rust_meta,
        ],
    )
    api.project.update_meta(project.id, meta.to_json())

    dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

    for item in os.listdir(dataset_path):
        subfolder = os.path.join(dataset_path, item)
        if dir_exists(subfolder):
            subfolder_tag_meta = subfolder_to_tag[item]
            images_names = [
                im_name for im_name in os.listdir(subfolder) if get_file_ext(im_name) == images_ext
            ]

            progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

            for images_names_batch in sly.batched(images_names, batch_size=batch_size):
                images_pathes_batch = [
                    os.path.join(subfolder, im_name) for im_name in images_names_batch
                ]

                img_infos = api.image.upload_paths(
                    dataset.id, images_names_batch, images_pathes_batch
                )
                img_ids = [im_info.id for im_info in img_infos]

                anns = [create_ann(image_path) for image_path in images_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

                progress.iters_done_report(len(images_names_batch))

    return project
