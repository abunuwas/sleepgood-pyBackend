













SELECT oauth_id, access_token, expiry, refresh_token, user_id FROM oauth WHERE (access_token = ?)

SELECT user_id, auto_login_ip, bankname, bic_swift, blz, comment, customer_id, date_format, date_last_login, date_registration, email, firstname, gender, iban, konto_inhaber, konto_nr, lastname, locale, max_alert_events, password, salt, session_id, settings, status, timezone, use_salt, username, vat, business_address_id, home_address_id FROM webuser WHERE (user_id = ?)

SELECT ship_id, best_photo_id, d_build_end, callsign, country_id, d_my_vessel_type, d_dwt, dest_port_id, dim_a, dim_c, dim_d, dim_b, d_gross_tonnage, imo, last_course, last_destination, last_draught, last_eta, last_port_id, last_position, last_seen, last_speed, length, d_draft_summer, mmsi, name, d_service_speed, servicestatus_id, shiptype_id, d_teu, time_created, time_updated, to_delete, valid, width, wrong_imo FROM ship WHERE (ship_id = ?)

SELECT t1.myvessel_id, t1.color_in_cockpit, t1.my_vessel_group_id, t1.note, t1.pos_report, t1.ship_id, t1.show_in_cockpit, t1.time_created, t1.user_id, t0.ship_id, t0.best_photo_id, t0.d_build_end, t0.callsign, t0.country_id, t0.d_my_vessel_type, t0.d_dwt, t0.dest_port_id, t0.dim_a, t0.dim_c, t0.dim_d, t0.dim_b, t0.d_gross_tonnage, t0.imo, t0.last_course, t0.last_destination, t0.last_draught, t0.last_eta, t0.last_port_id, t0.last_position, t0.last_seen, t0.last_speed, t0.length, t0.d_draft_summer, t0.mmsi, t0.name, t0.d_service_speed, t0.servicestatus_id, t0.shiptype_id, t0.d_teu, t0.time_created, t0.time_updated, t0.to_delete, t0.valid, t0.width, t0.wrong_imo, t2.user_id, t2.auto_login_ip, t2.bankname, t2.bic_swift, t2.blz, t2.comment, t2.customer_id, t2.date_format, t2.date_last_login, t2.date_registration, t2.email, t2.firstname, t2.gender, t2.iban, t2.konto_inhaber, t2.konto_nr, t2.lastname, t2.locale, t2.max_alert_events, t2.password, t2.salt, t2.session_id, t2.settings, t2.status, t2.timezone, t2.use_salt, t2.username, t2.vat, t2.business_address_id, t2.home_address_id FROM ship t0, webuser t2, myvessel t1 WHERE (((t1.ship_id = ?) AND (t1.user_id = ?)) AND ((t0.ship_id = t1.ship_id) AND (t2.user_id = t1.user_id)))

SELECT latest_unique_position_id, actiontype_id, navigational_status, anchorage_id, berth_id, cog, datasource_id, datasource_id_static, dest_port_id, destination_text, draught, eta, port_id, position, rot, ship_id, sog, time_of_actiontype_change, time_seen, time_seen_static, time_updated, heading FROM latest_unique_position WHERE (ship_id = ?)

SELECT * FROM area where not st_isempty(geometry) and st_contains(geometry,st_geomfromText(?)) order by layer asc limit 1

SELECT port_id, alertable, best_photo_id, contact_info, country_id, created_user_id, deleted, geodata, livecockpit, locode, lookat, major_port, mobile_demo, name, STATIONSNR, time_created, time_updated, time_upload_geodata, TIMEZONE, updated_user_id, vname FROM port WHERE (port_id = ?)

SELECT oauth_id, access_token, expiry, refresh_token, user_id FROM oauth WHERE (access_token = ?)

SELECT user_id, auto_login_ip, bankname, bic_swift, blz, comment, customer_id, date_format, date_last_login, date_registration, email, firstname, gender, iban, konto_inhaber, konto_nr, lastname, locale, max_alert_events, password, salt, session_id, settings, status, timezone, use_salt, username, vat, business_address_id, home_address_id FROM webuser WHERE (user_id = ?)

SELECT g.my_vessel_group_id as group_id, g.name as group_name, g.my_vessel_group_id as id, g.show_in_cockpit as group_show, null as vessel_show, null as vessel_name, null as vessel_id, null as vessel_color, null as vessel_status, null as vessel_last_seen, null as vessel_last_position, g.color as group_color from my_vessel_group g where g.user_id = ? 

select g.my_vessel_group_id as group_id, g.name as group_name, g.show_in_cockpit as group_show, v.show_in_cockpit as vessel_show, v.myvessel_id as id, s.name as vessel_name, s.ship_id as vessel_id, s.servicestatus_id as vessel_status, s.last_seen as vessel_last_seen, s.last_position as vessel_last_position, v.color_in_cockpit as vessel_color, g.color as group_color from myvessel v left outer join my_vessel_group g on g.my_vessel_group_id = v.my_vessel_group_id left join ship s on s.ship_id = v.ship_id inner join latest_unique_position l on l.ship_id = s.ship_id where v.user_id = ?

SELECT oauth_id, access_token, expiry, refresh_token, user_id FROM oauth WHERE (access_token = ?)

SELECT user_id, auto_login_ip, bankname, bic_swift, blz, comment, customer_id, date_format, date_last_login, date_registration, email, firstname, gender, iban, konto_inhaber, konto_nr, lastname, locale, max_alert_events, password, salt, session_id, settings, status, timezone, use_salt, username, vat, business_address_id, home_address_id FROM webuser WHERE (user_id = ?)

SELECT g.my_vessel_group_id as group_id, g.name as group_name, g.show_in_cockpit as group_show, v.show_in_cockpit as vessel_show, v.myvessel_id as id, s.name as vessel_name, s.ship_id as vessel_id, s.servicestatus_id as vessel_status, s.last_seen as vessel_last_seen, s.last_position as vessel_last_position, v.color_in_cockpit as vessel_color, g.color as group_color from myvessel v left outer join my_vessel_group g on g.my_vessel_group_id = v.my_vessel_group_id left join ship s on s.ship_id = v.ship_id inner join latest_unique_position l on l.ship_id = s.ship_id where v.user_id = ? and s.ship_id = ?

SELECT oauth_id, access_token, expiry, refresh_token, user_id FROM oauth WHERE (access_token = ?)

SELECT user_id, auto_login_ip, bankname, bic_swift, blz, comment, customer_id, date_format, date_last_login, date_registration, email, firstname, gender, iban, konto_inhaber, konto_nr, lastname, locale, max_alert_events, password, salt, session_id, settings, status, timezone, use_salt, username, vat, business_address_id, home_address_id FROM webuser WHERE (user_id = ?)

SELECT t1.rel_vt_permission_webuser_id, t1.vt_permission_id, t1.settings, t1.user_id FROM rel_vt_permission_webuser t1 LEFT OUTER JOIN webuser t0 ON (t0.user_id = t1.user_id) WHERE (t1.user_id = ?)

SELECT vt_permission_id, description, name, structure FROM vt_permission WHERE (vt_permission_id = ?)

SELECT user_id, auto_login_ip, bankname, bic_swift, blz, comment, customer_id, date_format, date_last_login, date_registration, email, firstname, gender, iban, konto_inhaber, konto_nr, lastname, locale, max_alert_events, password, salt, session_id, settings, status, timezone, use_salt, username, vat, business_address_id, home_address_id FROM webuser WHERE (user_id = ?)

SELECT t1.ship_id AS a1, t1.best_photo_id AS a2, t1.d_build_end AS a3, t1.callsign AS a4, t1.country_id AS a5, t1.d_my_vessel_type AS a6, t1.d_dwt AS a7, t1.dest_port_id AS a8, t1.dim_a AS a9, t1.dim_c AS a10, t1.dim_d AS a11, t1.dim_b AS a12, t1.d_gross_tonnage AS a13, t1.imo AS a14, t1.last_course AS a15, t1.last_destination AS a16, t1.last_draught AS a17, t1.last_eta AS a18, t1.last_port_id AS a19, t1.last_position AS a20, t1.last_seen AS a21, t1.last_speed AS a22, t1.length AS a23, t1.d_draft_summer AS a24, t1.mmsi AS a25, t1.name AS a26, t1.d_service_speed AS a27, t1.servicestatus_id AS a28, t1.shiptype_id AS a29, t1.d_teu AS a30, t1.time_created AS a31, t1.time_updated AS a32, t1.to_delete AS a33, t1.valid AS a34, t1.width AS a35, t1.wrong_imo AS a36, t0.latest_unique_position_id AS a37, t0.actiontype_id AS a38, t0.navigational_status AS a39, t0.anchorage_id AS a40, t0.berth_id AS a41, t0.cog AS a42, t0.datasource_id AS a43, t0.datasource_id_static AS a44, t0.dest_port_id AS a45, t0.destination_text AS a46, t0.draught AS a47, t0.eta AS a48, t0.port_id AS a49, t0.position AS a50, t0.rot AS a51, t0.ship_id AS a52, t0.sog AS a53, t0.time_of_actiontype_change AS a54, t0.time_seen AS a55, t0.time_seen_static AS a56, t0.time_updated AS a57, t0.heading AS a58, t2.port_id AS a59, t2.alertable AS a60, t2.best_photo_id AS a61, t2.contact_info AS a62, t2.country_id AS a63, t2.created_user_id AS a64, t2.deleted AS a65, t2.geodata AS a66, t2.livecockpit AS a67, t2.locode AS a68, t2.lookat AS a69, t2.major_port AS a70, t2.mobile_demo AS a71, t2.name AS a72, t2.STATIONSNR AS a73, t2.time_created AS a74, t2.time_updated AS a75, t2.time_upload_geodata AS a76, t2.TIMEZONE AS a77, t2.updated_user_id AS a78, t2.vname AS a79 FROM latest_unique_position t0 LEFT OUTER JOIN port t2 ON (t2.port_id = t0.dest_port_id), ship t1 WHERE (((st_contains(st_makeenvelope(?, ?, ?, ?, ?), t0.position) AND (t0.time_updated >= ?)) AND (t1.length <= ?)) AND (t0.ship_id = t1.ship_id)) ORDER BY t1.length DESC NULLS LAST LIMIT ? OFFSET ?SELECT COUNT(t0.ship_id) FROM ship t0, latest_unique_position t1 WHERE ((((t1.time_updated >= ?) AND (t0.length <= ?)) AND st_contains(st_makeenvelope(?, ?, ?, ?, ?), t1.position)) AND (t1.ship_id = t0.ship_id))
