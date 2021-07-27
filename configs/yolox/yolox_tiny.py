_base_ = './yolox_s.py'

# model settings
model = dict(
    backbone=dict(depth=0.33, width=0.375),
    bbox_head=dict(width=0.375)
)

img_norm_cfg = dict(mean=[0.485 * 255, 0.456 * 255, 0.406 * 255], std=[0.229 * 255, 0.224 * 255, 0.225 * 255],
                    to_rgb=True)
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(416, 416),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Pad', size=(416, 416), pad_val=114.0),
            dict(type='Normalize', **img_norm_cfg),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img'])
        ])
]

# close mixup
train_dataset = dict(
    mosaic_pipeline=[],
    enable_mixup=False)

data = dict(
    train=dict(pipeline=train_dataset),
    test=dict(pipeline=test_pipeline),
    val=dict(pipeline=test_pipeline))

resume_from = None

interval = 10
evaluation = dict(interval=interval, metric='bbox')
# random_size=(10, 20)
custom_hooks = [
    dict(
        type='YoloXProcessHook',
        random_size=(10, 20),
        no_aug_epoch=15,
        eval_interval=interval,
        priority=48),
    dict(type='EMAHook', priority=49, resume_from=resume_from)
]
log_config = dict(interval=50)
checkpoint_config = dict(interval=interval)

