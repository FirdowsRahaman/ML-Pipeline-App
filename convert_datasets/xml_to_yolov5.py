import os
import shutil
import random
import xml.etree.ElementTree as ET
from tqdm import tqdm
from xml.dom import minidom
from sklearn.model_selection import train_test_split


# Function to get the data from XML Annotation
def extract_info_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()
    
    # Initialise the info dict 
    info_dict = {}
    info_dict['bboxes'] = []

    # Parse the XML Tree
    for elem in root:
        # Get the file name 
        if elem.tag == "filename":
            info_dict['filename'] = elem.text
            
        # Get the image size
        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))
            
            info_dict['image_size'] = tuple(image_size)
        
        # Get details of the bounding box 
        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                    
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)            
            info_dict['bboxes'].append(bbox)
    
    return info_dict
  
  
  # Dictionary that maps class names to IDs
class_name_to_id_mapping = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
                            'A': 10, 'B': 11,'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18,
                            'J': 19, 'K': 20, 'L': 21, 'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26, 'R': 27, 
                            'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35
                           }


# Convert the info dict to the required yolo format and write it to disk
def convert_to_yolov5(info_dict, ann):
    print_buffer = []
    
    # For each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid Class. Must be one from ", class_name_to_id_mapping.keys())
        
        # Transform the bbox co-ordinates as per the format required by YOLO v5
        b_center_x = (b["xmin"] + b["xmax"]) / 2 
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width    = (b["xmax"] - b["xmin"])
        b_height   = (b["ymax"] - b["ymin"])
        
        # Normalise the co-ordinates by the dimensions of the image
        image_w, image_h, image_c = info_dict["image_size"]  
        b_center_x /= image_w 
        b_center_y /= image_h 
        b_width    /= image_w 
        b_height   /= image_h 
        
        #Write the bbox details to the file 
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))
    
    xml_file = os.path.split(ann)[-1]
    # Name of the file which we have to save 
#     save_file_name = os.path.join("Char_Detect_YOLOv5_Dataset", xml_file.replace("xml", "txt"))
    save_file_name = os.path.join("test_Dataset", xml_file.replace("xml", "txt"))
    
    # Save the annotation to disk
    print("\n".join(print_buffer), file= open(save_file_name, "w"))
    
    
    # Get the annotations
# annotations = [os.path.join('train_annotations_dir', x) for x in os.listdir('train_annotations_dir') if x[-3:] == "xml"]
annotations = [os.path.join('test/annotations_dir', x) for x in os.listdir('test/annotations_dir') if x[-3:] == "xml"]
# annotations.sort()

# Convert and save the annotations
for ann in tqdm(annotations):
    info_dict = extract_info_from_xml(ann)
    convert_to_yolov5(info_dict, ann)
annotations = [os.path.join('test_Dataset', x) for x in os.listdir('test_Dataset') if x[-3:] == "txt"]

# # Read images and annotations
# images = [os.path.join('train_image_dir', x) for x in os.listdir('train_image_dir')]
# annotations = [os.path.join('Char_Detect_YOLOv5_Dataset', x) for x in os.listdir('Char_Detect_YOLOv5_Dataset') if x[-3:] == "txt"]

# images.sort()
# annotations.sort()

# # Split the dataset into train-valid-test splits 
# train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size = 0.2, random_state = 1)
# # val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations, test_size = 0.5, random_state = 1)

test_images = [os.path.join('test/image_dir', x) for x in os.listdir('test/image_dir')]
test_annotations = [os.path.join('test_Dataset', x) for x in os.listdir('test_Dataset') if x[-3:] == "txt"]

images.sort()
annotations.sort()

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val/')
# move_files_to_folder(test_images, 'images/test/')
move_files_to_folder(train_annotations, 'labels/train/')
move_files_to_folder(val_annotations, 'labels/val/')
# move_files_to_folder(test_annotations, 'annotations/test/')

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

            
# Move the splits into their folders
move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val/')
move_files_to_folder(test_images, 'Char_Detect_YOLOv5_Dataset/images/test/')
move_files_to_folder(train_annotations, 'labels/train/')
move_files_to_folder(val_annotations, 'labels/val/')
move_files_to_folder(test_annotations, 'Char_Detect_YOLOv5_Dataset/labels/test/')

