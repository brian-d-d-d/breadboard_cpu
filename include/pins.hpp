#ifndef PINS_HPP
#define PINS_HPP

#include <stdint.h>

#define DEFAULT_BUS_LEN 8

const int BUS_1[] = {39, 41, 43, 45, 47, 49, 51, 53};
const int BUS_2[] = {23, 25, 27, 29, 31, 33, 35, 37};
const int BUS_3[] = {2, 3, 4, 5, 6, 7, 8, 9};

#define BUS_1_LEN sizeof(BUS_1) / sizeof(int)
#define BUS_2_LEN sizeof(BUS_2) / sizeof(int)
#define BUS_3_LEN sizeof(BUS_3) / sizeof(int)

void bus_set_mode(char mode, const int bus[], int bus_len = DEFAULT_BUS_LEN);

void bus_set_pin_mode(char mode, const int bus[], int index);

void bus_set_byte_value(uint8_t value, const int bus[], int bus_len = DEFAULT_BUS_LEN);

void bus_set_bit_value(uint8_t value, const int bus[], int index);

uint8_t bus_get_byte_value(const int bus[], int bus_len = DEFAULT_BUS_LEN);

uint8_t bus_get_bit_value(const int bus[], int index);

#endif