CREATE TABLE waitingtime (
    id SERIAL PRIMARY KEY,
    t2WaitingTime int NOT NULL,
    t2WaitingTimeInterval character varying(255) NOT NULL,
    deliveryId timestamp with time zone DEFAULT
);
