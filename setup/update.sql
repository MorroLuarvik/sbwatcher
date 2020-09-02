/*********************************
** 2020.09.02                   **
*********************************/

USE `sbwatcher`;

ALTER TABLE `a_events`
    ADD `mode_id`  TINYINT UNSIGNED NOT NULL DEFAULT 0
        AFTER `rate_id`,
    ADD KEY `mode_id_idx` (`mode_id`) USING BTREE;

ALTER TABLE `a_events`
    DROP KEY `event_idx`,
    ADD UNIQUE KEY `event_idx` (`fin_id`, `rate_id`, `mode_id`) USING BTREE;
