CREATE TABLE alert (
    id integer primary key autoincrement not null,
    sent int not null,
    created_at text not null,
    device_type text not null,
    device_id text not null,
    device_deployed_on text not null,
    longitude real not null,
    latitude real not null,
    face_model_name text not null,
    face_model_guid text not null,
    face_model_threshold real not null,
    mask_model_name text not null,
    mask_model_guid text not null,
    mask_model_threshold real not null,
    probability real not null,
    image_format text not null,
    image_width int not null,
    image_height int not null,
    image_data blob not null
);


SELECT * from alert;