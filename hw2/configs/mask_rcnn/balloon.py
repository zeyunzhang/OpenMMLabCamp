_base_ = ["mask_rcnn_r50_fpn_2x_coco.py"]

data=dict(
        samples_per_gpu=8,
        train = dict(
                ann_file = "data/balloon/annotations/train.json",
                img_prefix="data/balloon/train",
                classes = ("balloon",)
                
            ), 
        val = dict(
                ann_file = "data/balloon/annotations/val.json",
                img_prefix="data/balloon/val",
                classes = ("balloon",)
            ),
        test = dict(
                ann_file = "data/balloon/annotations/val.json",
                img_prefix="data/balloon/val",
                classes = ("balloon",)
            )
        )
model = dict(roi_head=dict(bbox_head=dict(num_classes=1), mask_head=dict(num_classes=1)))

runner = dict(type="EpochBasedRunner", max_epochs=24)

optimizer = dict(type="SGD", lr=0.001)

lr_config = None

log_config=dict(interval=25, hooks=[dict(type="TextLoggerHook")])

load_from = "checkpoints/mask_rcnn_r50_fpn_2x_coco_bbox_mAP-0.392__segm_mAP-0.354_20200505_003907-3e542a40.pth"

evaluation = dict(metric=['segm'])
