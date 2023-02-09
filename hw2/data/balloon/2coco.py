import json
import datetime
from PIL import Image

"""
{
    "info": info,
    "licenses": [license],
    "images": [image],
    "annotations": [annotation],
    "categories": [category]
}

"info":{
	"description":"This is stable 1.0 version of the 2014 MS COCO dataset.",
	"url":"http:\/\/mscoco.org",
	"version":"1.0","year":2014,
	"contributor":"Microsoft COCO group",
	"date_created":"2015-01-27 09:11:52.357475"
},

image {
    "id" : int,
    "width" : int,
    "height" : int,
    "file_name" : str,
    "license" : int,
    "flickr_url" : str,
    "coco_url" : str,
    "date_captured" : datetime
}

annotation{
    "id": int,    
    "image_id": int,
    "category_id": int,
    "segmentation": RLE or [polygon],
    "area": float,
    "bbox": [x,y,width,height],
    "iscrowd": 0 or 1,
}


"""
def getImageSize(img_path):
    img = Image.open(img_path)
    size = img.size  #大小/尺寸
    w = img.width       #图片的宽
    h = img.height      #图片的高
    f = img.format      #图像格式
    return (size, w, h)

json_file= "via_region_data.json"

categories = [
    {
	    "supercategory": "balloon",
	    "id": 1,
	    "name": "balloon"
    },
    {
	    "supercategory": "other",
	    "id": 2,
	    "name": "other"
    }
]

images = []
image = {}
annotations = []
ann = {}

with open(json_file) as balloon:

    image_id = 1 #increment 
    mask_id = 1 
    balloon_json = json.load(balloon)
    #print(balloon_json)
    for _,value in balloon_json.items():
        filename = value["filename"]
        file_size = value["size"]

        img_size, w, h = getImageSize(filename)
        print("size: {}, img_size: {}, width: {}, height: {}".format(file_size, img_size, w, h))
        
        image["id"] = image_id
        image["file_name"] = filename
        image["width"] = w
        image["height"] = h
        image["license"] = ""
        image["flickr_url"] = ""
        image["coco_url"] = ""
        image["date_captured"] = str(datetime.datetime.now())
        image["license"] = 3
        images.append(image.copy())

        regions = value["regions"]
        #iscrowd = 1 if len(regions) > 1 else 0
        iscrowd = 0
        for key, shape in regions.items():
            ann["id"] = mask_id
            mask_id +=1
            ann["image_id"] = image_id
            ann["category_id"] = 1
            
            ann["iscrowd"] = iscrowd
            # for segmentation
            all_points_x = shape["shape_attributes"]["all_points_x"]
            all_points_y = shape["shape_attributes"]["all_points_y"]
            segmentation = []
            for i in range(len(all_points_x)):
                segmentation.extend([all_points_x[i], all_points_y[i]])
            ann["segmentation"] = [segmentation]

            # get bbox from segmentation
            minX = min(all_points_x)
            maxX = max(all_points_x)
            minY = min(all_points_y)
            maxY = max(all_points_y)

            bbox_w = maxX - minX
            bbox_h = maxY - minY

            ann["bbox"] = [minX, minY, bbox_w, bbox_h]
            area = bbox_w * bbox_h
            ann["area"] = area
            print("bbox: ({}, {}, {}, {}), area: {}".format(minX, minY, bbox_w, bbox_h, area))

            annotations.append(ann.copy())

        image_id = image_id + 1 

coco = {}

"""
"info":{
	"description":"This is stable 1.0 version of the 2014 MS COCO dataset.",
	"url":"http:\/\/mscoco.org",
	"version":"1.0","year":2014,
	"contributor":"Microsoft COCO group",
	"date_created":"2015-01-27 09:11:52.357475"
}
"""
info = {}
info["description"] = "test"
info["url"] = "http://test.org"
info["version"] = "1.0"
info["contributor"] = "Richardz"
info["date_created"] = "2015-01-27 09:11:52.357475"

coco["info"] = info
coco["images"] = images
coco["categories"] = categories
coco["annotations"] = annotations

with open("./val_coco.json", "w") as coco_file:
    json.dump(coco, coco_file)
