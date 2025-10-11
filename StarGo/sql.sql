insert into app_users (username, password, role, created_at) VALUES
('user1', '12345', 'user', now()),
('user2', '12345', 'user', now());

INSERT INTO app_places (name, googlemaplink, address, imageurl, created_at, addby_users_id) VALUES
('Mega Bangna', '', '38/1-3 39 หมู่ที่ 6 ทางคู่ขนาน ถนนบางนา-ตราด ตำบล บางแก้ว อำเภอบางพลี สมุทรปราการ 10540', null, now(), 2),
('Ratwinit Bangkaeo', '', '31 หมู่ 13 ซอย เมืองแก้ว 4 ตำบล บางแก้ว อำเภอบางพลี สมุทรปราการ 10540', null, now(), 2);

insert into app_celebrities (firstname, lastname, nickname, imageurl, created_at, addby_users_id) VALUES
('testceleb1', 'testceleb1', 'celeb1', null, now(), 2),
('testceleb2', 'testceleb2', 'celeb2', null, now(), 2);

insert into app_sightings (arrivaldate, created_at, celebrities_id, places_id, addby_users_id) VALUES
('2023-10-01', now(), 1, 2, 2),
('2023-10-02', now(), 1, 3, 2),
('2023-10-03', now(), 2, 2, 2);

insert into app_groups (name, description, company, datestartgroup, created_at, addby_users_id) VALUES
('Group1', 'Description for Group1', 'Company1', '2023-10-01', now(), 2),
('Group2', 'Description for Group2', 'Company2', '2023-10-02', now(), 2);

-- Reset the sequence for app_sightings id to avoid conflicts
SELECT setval(
  pg_get_serial_sequence('app_sightings', 'id'),
  COALESCE(MAX(id), 0) + 1,
  false
) FROM app_sightings;

SELECT setval(
  pg_get_serial_sequence('app_groups', 'id'),
  COALESCE(MAX(id), 0) + 1,
  false
) FROM app_groups;

SELECT setval(
  pg_get_serial_sequence('auth_user', 'id'),
  COALESCE(MAX(id), 0) + 1,
  false
) FROM auth_user;