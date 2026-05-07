#include <Arduino.h>

#include "pins.hpp"
#include "interface.hpp"

void setup() {
    Serial.begin(9600);

    bus_set_mode(OUTPUT, BUS_0);
    bus_set_mode(OUTPUT, BUS_1);
    bus_set_mode(OUTPUT, BUS_2);
}


void loop() {
    serial_receive();

    // int delay_ms = 100;
    // uint8_t val = 0x01;

    // for (int i = 0; i < 8; i++) {
    //     bus_set_byte_value(val, BUS_1);
    //     bus_set_byte_value(val, BUS_2);
    //     bus_set_byte_value(val, BUS_3);
    //     val <<= 1;

    //     delay(delay_ms);
    // }

    // val = 0x40;

    // for (int i = 0; i < 6; i++) {
    //     bus_set_byte_value(val, BUS_1, BUS_1_LEN);
    //     bus_set_byte_value(val, BUS_2);
    //     bus_set_byte_value(val, BUS_3);
    //     val >>= 1;

    //     delay(delay_ms);
    // }
}