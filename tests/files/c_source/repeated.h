/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2019 Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/**
 * This file was generated by pbtools version 0.2.0 Tue Aug 27 22:08:14 2019.
 */

#ifndef REPEATED_H
#define REPEATED_H

#include "pbtools.h"

/**
 * Message Message in package repeated.
 */
struct repeated_message_message_repeated_t {
    int length;
    struct repeated_message_t **items_pp;
    struct repeated_message_t *head_p;
    struct repeated_message_t *tail_p;
};

struct repeated_message_t {
    struct pbtools_heap_t *heap_p;
    struct repeated_message_t *next_p;
    struct pbtools_repeated_int32_t int32s;
    struct repeated_message_message_repeated_t messages;
    struct pbtools_repeated_string_t strings;
    struct pbtools_repeated_bytes_t bytes;
};

int repeated_message_int32s_alloc(
    struct repeated_message_t *self_p,
    int length);

int repeated_message_messages_alloc(
    struct repeated_message_t *self_p,
    int length);

int repeated_message_strings_alloc(
    struct repeated_message_t *self_p,
    int length);

int repeated_message_bytes_alloc(
    struct repeated_message_t *self_p,
    int length);

/**
 * Create a new message Message in given workspace.
 *
 * @param[in] workspace_p Message workspace.
 * @param[in] size Workspace size.
 *
 * @return Initialized address book, or NULL on failure.
 */
struct repeated_message_t *repeated_message_new(
    void *workspace_p,
    size_t size);

/**
 * Encode message Message defined in package repeated.
 *
 * @param[in] self_p Message to encode.
 * @param[out] encoded_p Buffer to encode the message into.
 * @param[in] size Encoded buffer size.
 *
 * @return Encoded data length or negative error code.
 */
int repeated_message_encode(
    struct repeated_message_t *self_p,
    uint8_t *encoded_p,
    size_t size);

/**
 * Decode message Message defined in package repeated.
 *
 * @param[in,out] self_p Initialized message to decode into.
 * @param[in] encoded_p Buffer to decode.
 * @param[in] size Size of the encoded message.
 *
 * @return Number of bytes decoded or negative error code.
 */
int repeated_message_decode(
    struct repeated_message_t *self_p,
    const uint8_t *encoded_p,
    size_t size);

#endif
