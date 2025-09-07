/*****************************CS**********************************************//**
 * @file
 * @brief ICM40627 Config
 *******************************************************************************
 * # License
 * <b>Copyright 2024 Silicon Laboratories Inc. www.silabs.com</b>
 *******************************************************************************
 *
 * SPDX-License-Identifier: Zlib
 *
 * The licensor of this software is Silicon Laboratories Inc.
 *
 * This software is provided 'as-is', without any express or implied
 * warranty. In no event will the authors be held liable for any damages
 * arising from the use of this software.
 *
 * Permission is granted to anyone to use this software for any purpose,
 * including commercial applications, and to alter it and redistribute it
 * freely, subject to the following restrictions:
 *
 * 1. The origin of this software must not be misrepresented; you must not
 *    claim that you wrote the original software. If you use this software
 *    in a product, an acknowledgment in the product documentation would be
 *    appreciated but is not required.
 * 2. Altered source versions must be plainly marked as such, and must not be
 *    misrepresented as being the original software.
 * 3. This notice may not be removed or altered from any source distribution.
 *
 ******************************************************************************/

#ifndef SL_ICM40627_CONFIG_H
#define SL_ICM40627_CONFIG_H

// <<< sl:start pin_tool >>>
// <eusart signal=TX,RX,SCLK,CS> SL_ICM40627_SPI_EUSART
// $[EUSART_SL_ICM40627_SPI_EUSART]
#ifndef SL_ICM40627_SPI_EUSART_PERIPHERAL       
#define SL_ICM40627_SPI_EUSART_PERIPHERAL        EUSART1
#endif
#ifndef SL_ICM40627_SPI_EUSART_PERIPHERAL_NO    
#define SL_ICM40627_SPI_EUSART_PERIPHERAL_NO     1
#endif

// EUSART1 TX on PC03
#ifndef SL_ICM40627_SPI_EUSART_TX_PORT          
#define SL_ICM40627_SPI_EUSART_TX_PORT           SL_GPIO_PORT_C
#endif
#ifndef SL_ICM40627_SPI_EUSART_TX_PIN           
#define SL_ICM40627_SPI_EUSART_TX_PIN            3
#endif

// EUSART1 RX on PC02
#ifndef SL_ICM40627_SPI_EUSART_RX_PORT          
#define SL_ICM40627_SPI_EUSART_RX_PORT           SL_GPIO_PORT_C
#endif
#ifndef SL_ICM40627_SPI_EUSART_RX_PIN           
#define SL_ICM40627_SPI_EUSART_RX_PIN            2
#endif

// EUSART1 SCLK on PC01
#ifndef SL_ICM40627_SPI_EUSART_SCLK_PORT        
#define SL_ICM40627_SPI_EUSART_SCLK_PORT         SL_GPIO_PORT_C
#endif
#ifndef SL_ICM40627_SPI_EUSART_SCLK_PIN         
#define SL_ICM40627_SPI_EUSART_SCLK_PIN          1
#endif

// EUSART1 CS on PC00
#ifndef SL_ICM40627_SPI_EUSART_CS_PORT          
#define SL_ICM40627_SPI_EUSART_CS_PORT           SL_GPIO_PORT_C
#endif
#ifndef SL_ICM40627_SPI_EUSART_CS_PIN           
#define SL_ICM40627_SPI_EUSART_CS_PIN            0
#endif
// [EUSART_SL_ICM40627_SPI_EUSART]$

// <gpio optional=true> SL_ICM40627_INT
// $[GPIO_SL_ICM40627_INT]
#ifndef SL_ICM40627_INT_PORT                    
#define SL_ICM40627_INT_PORT                     SL_GPIO_PORT_B
#endif
#ifndef SL_ICM40627_INT_PIN                     
#define SL_ICM40627_INT_PIN                      1
#endif
// [GPIO_SL_ICM40627_INT]$
// <<< sl:end pin_tool >>>

#endif // SL_ICM40627_CONFIG_H
