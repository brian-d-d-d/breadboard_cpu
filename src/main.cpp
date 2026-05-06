#include <Arduino.h>

#include <pins.hpp>


void setup() {
    Serial.begin(9600);

    set_bus_mode(OUTPUT, BUS_1, BUS_1_LEN);
    set_bus_mode(OUTPUT, BUS_2, BUS_2_LEN);
}


void loop() {
    set_bus_byte_value(0b11000011, BUS_1, BUS_1_LEN);
    set_bus_byte_value(0b11000011, BUS_2, BUS_2_LEN);

    delay(500);

    set_bus_byte_value(0b00111100, BUS_1, BUS_1_LEN);
    set_bus_byte_value(0b00111100, BUS_2, BUS_2_LEN);

    delay(500);
}