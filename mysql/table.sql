create table compressor_measurements
(
    id INT AUTO_INCREMENT PRIMARY KEY,
    moment DATETIME,
    voltage DOUBLE,
    current DOUBLE,
    power_W DOUBLE,
    energy_WH DOUBLE,
    power_factor_measured DOUBLE,
    power_factor_calc DOUBLE,
    phase_angle_measured DOUBLE,
    phase_angle_calc DOUBLE,
    opMode INT AS (
		CASE
			WHEN current >0.35 THEN 1
            ELSE 0
		END
    )
);
