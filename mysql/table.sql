CREATE TABLE `compressor_measurements` (
  `id` int NOT NULL AUTO_INCREMENT,
  `moment` datetime DEFAULT NULL,
  `voltage` double DEFAULT NULL,
  `current` double DEFAULT NULL,
  `power_W` double DEFAULT NULL,
  `energy_WH` double DEFAULT NULL,
  `power_factor_measured` double DEFAULT NULL,
  `power_factor_calc` double DEFAULT NULL,
  `phase_angle_measured` double DEFAULT NULL,
  `phase_angle_calc` double DEFAULT NULL,
  `opMode` int GENERATED ALWAYS AS ((case when (`current` > 28) then 3 when (`current` between 18 and 28) then 1 when (`current` between 3 and 18) then 2 else 0 end)) VIRTUAL,
  `week_year` varchar(7) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci GENERATED ALWAYS AS (concat(convert(substr(yearweek(`moment`,1),1,4) using utf8mb4),_utf8mb4'-',convert(substr(yearweek(`moment`,1),5,2) using utf8mb4))) VIRTUAL,
  `active_hours` tinyint(1) GENERATED ALWAYS AS ((case when (date_format(`moment`,_utf8mb4'%H:%i:%s') between _utf8mb4'23:00:00' and _utf8mb4'23:59:59') then 0 when (date_format(`moment`,_utf8mb4'%H:%i:%s') between _utf8mb4'00:00:00' and _utf8mb4'07:30:00') then 0 else 1 end)) VIRTUAL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4098541 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
