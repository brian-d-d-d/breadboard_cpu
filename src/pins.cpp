#include "pins.hpp"

#include <Arduino.h>

// Set all pins in the bus to mode
void set_bus_mode(char mode, const int bus[], int bus_len = DEFAULT_BUS_LEN) {
    for (int i = 0; i < bus_len; i++) {
        pinMode(bus[i], mode);
    }
}

// Set a specific pin at index in a bus to mode
void set_bus_pin_mode(char mode, const int bus[], int index) {
    pinMode(bus[index], mode);
}

//Sets the first 8 pins in a bus to value
void set_bus_byte_value(uint8_t value, const int bus[], int bus_len = DEFAULT_BUS_LEN) {
    if (bus_len > 8) {
        bus_len = 8;
    }
    
    for (int i = 0; i < bus_len; i++) {
        uint8_t bit_value = (0x01 << i) & value;
        uint8_t val = (bit_value == 0 ? LOW : HIGH);

        digitalWrite(bus[i], val);
    }
}

//Sets a specific pin at index in a bus to value. Value should be LOW (0) or HIGH (1)
void set_bus_bit_value(uint8_t value, const int bus[], int index) {
    digitalWrite(bus[index], value);
}

//Gets the first 8 pins in a bus
uint8_t get_bus_byte_value(const int bus[], int bus_len = DEFAULT_BUS_LEN) {
    if (bus_len > 8) {
        bus_len = 8;
    }

    uint8_t val = 0x00;

    for (int i = 0; i < bus_len; i++) {
        uint8_t bit_value = (digitalRead(bus[i]) << i);
        val |= bit_value;
    }

    return val;
}

//Gets the bit at a specific pin on the bus
uint8_t get_bus_bit_value(const int bus[], int index) {
    return digitalRead(bus[index]);
}