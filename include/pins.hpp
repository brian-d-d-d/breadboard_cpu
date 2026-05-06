#ifndef PINS_H
#define PINS_H

#include <stdint.h>

#define DEFAULT_BUS_LEN 8

const int BUS_1[] = {39, 41, 43, 45, 47, 49, 51, 53};
const int BUS_2[] = {23, 25, 27, 29, 31, 33, 35, 37};

#define BUS_1_LEN sizeof(BUS_1) / sizeof(int)
#define BUS_2_LEN sizeof(BUS_2) / sizeof(int)

void set_bus_mode(char mode, const int bus[], int bus_len = DEFAULT_BUS_LEN);

void set_bus_pin_mode(char mode, const int bus[], int index);

void set_bus_byte_value(uint8_t value, const int bus[], int bus_len = DEFAULT_BUS_LEN);

void set_bus_bit_value(uint8_t value, const int bus[], int index);

uint8_t get_bus_byte_value(const int bus[], int bus_len = DEFAULT_BUS_LEN);

uint8_t get_bus_bit_value(const int bus[], int index);

#endif