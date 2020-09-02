/*********************************
** 2020.09.02                   **
*********************************/

USE `sbwatcher`;

ALTER TABLE `a_events`
    ADD `mode_id`  TINYINT UNSIGNED NOT NULL DEFAULT 0
        AFTER `rate_id`,
    ADD KEY `mode_id_idx` (`mode_id`) USING BTREE;
