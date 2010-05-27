//
// Copyright 2010 Ettus Research LLC
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

#ifndef INCLUDED_UHD_USRP_DBOARD_IFACE_HPP
#define INCLUDED_UHD_USRP_DBOARD_IFACE_HPP

#include <uhd/config.hpp>
#include <uhd/types/serial.hpp>
#include <boost/shared_ptr.hpp>
#include <boost/cstdint.hpp>

namespace uhd{ namespace usrp{

/*!
 * The daughter board dboard interface to be subclassed.
 * A dboard instance interfaces with the mboard though this api.
 * This interface provides i2c, spi, gpio, atr, aux dac/adc access.
 * Each mboard should have a specially tailored iface for its dboard.
 */
class UHD_API dboard_iface{
public:
    typedef boost::shared_ptr<dboard_iface> sptr;

    //tells the host which unit to use
    enum unit_t{
        UNIT_RX = 'r',
        UNIT_TX = 't'
    };

    //possible atr registers
    enum atr_reg_t{
        ATR_REG_IDLE        = 'i',
        ATR_REG_TX_ONLY     = 't',
        ATR_REG_RX_ONLY     = 'r',
        ATR_REG_FULL_DUPLEX = 'f'
    };

    /*!
     * Write to an aux dac.
     *
     * \param unit which unit rx or tx
     * \param which_dac the dac index 0, 1, 2, 3...
     * \param value the value in volts
     */
    virtual void write_aux_dac(unit_t unit, int which_dac, float value) = 0;

    /*!
     * Read from an aux adc.
     *
     * \param unit which unit rx or tx
     * \param which_adc the adc index 0, 1, 2, 3...
     * \return the value in volts
     */
    virtual float read_aux_adc(unit_t unit, int which_adc) = 0;

    /*!
     * Set a daughterboard output pin control source.
     * By default, the outputs are all GPIO controlled.
     *
     * \param unit which unit rx or tx
     * \param value 16-bits, 0=GPIO controlled, 1=ATR controlled
     */
    virtual void set_pin_ctrl(unit_t unit, boost::uint16_t value) = 0;

    /*!
     * Set a daughterboard ATR register.
     *
     * \param unit which unit rx or tx
     * \param reg which ATR register to set
     * \param value 16-bits, 0=ATR output low, 1=ATR output high
     */
    virtual void set_atr_reg(unit_t unit, atr_reg_t reg, boost::uint16_t value) = 0;

    /*!
     * Set daughterboard GPIO data direction register.
     * By default, the GPIO pins are all inputs.
     *
     * \param unit which unit rx or tx
     * \param value 16-bits, 0=GPIO input, 1=GPIO output
     */
    virtual void set_gpio_ddr(unit_t unit, boost::uint16_t value) = 0;

    /*!
     * Read daughterboard GPIO pin values.
     *
     * \param unit which unit rx or tx
     * \param value 16-bits, 0=GPIO output low, 1=GPIO output high
     */
    virtual void write_gpio(unit_t unit, boost::uint16_t value) = 0;

    /*!
     * Read daughterboard GPIO pin values.
     *
     * \param unit which unit rx or tx
     * \return the value of the gpio unit
     */
    virtual boost::uint16_t read_gpio(unit_t unit) = 0;

    /*!
     * Write to an I2C peripheral.
     *
     * \param addr I2C bus address (7-bits)
     * \param bytes the data to write
     */
    virtual void write_i2c(boost::uint8_t addr, const byte_vector_t &bytes) = 0;

    /*!
     * Read from an I2C peripheral.
     *
     * \param addr I2C bus address (7-bits)
     * \param num_bytes number of bytes to read
     * \return the data read if successful, else a zero length string.
     */
    virtual byte_vector_t read_i2c(boost::uint8_t addr, size_t num_bytes) = 0;

    /*!
     * Write data to SPI bus peripheral.
     *
     * \param unit which unit, rx or tx
     * \param config configuration settings
     * \param data the bits to write LSB first
     * \param num_bits the number of bits in data
     */
    virtual void write_spi(
        unit_t unit,
        const spi_config_t &config,
        boost::uint32_t data,
        size_t num_bits
    ) = 0;

    /*!
     * Read and write data to SPI bus peripheral.
     *
     * \param unit which unit, rx or tx
     * \param config configuration settings
     * \param data the bits to write LSB first
     * \param num_bits the number of bits in data
     * \return the data that was read
     */
    virtual boost::uint32_t read_write_spi(
        unit_t unit,
        const spi_config_t &config,
        boost::uint32_t data,
        size_t num_bits
    ) = 0;

    /*!
     * Get the rate of a dboard clock.
     *
     * \param unit which unit rx or tx
     * \return the clock rate in Hz
     */
    virtual double get_clock_rate(unit_t unit) = 0;

    /*!
     * Enable or disable a dboard clock.
     *
     * \param unit which unit rx or tx
     * \param enb true for enabled
     */
    virtual void set_clock_enabled(unit_t unit, bool enb) = 0;
};

}} //namespace

#endif /* INCLUDED_UHD_USRP_DBOARD_IFACE_HPP */
