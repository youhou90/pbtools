import re


PRIMITIVE_TYPES = [
    'int32',
    'int64',
    'sint32',
    'sint64',
    'uint32',
    'uint64',
    'fixed32',
    'fixed64',
    'sfixed32',
    'sfixed64',
    'float',
    'double',
    'bool',
    'string',
    'bytes'
]

HEADER_FMT = '''\
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
 * This file was generated by pbtools.
 */

#ifndef {include_guard}
#define {include_guard}

#include "pbtools.h"

{structs}
{declarations}
#endif
'''

SOURCE_FMT = '''\
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
 * This file was generated by pbtools.
 */

#include "{header}"

{definitions}\
'''

MESSAGE_STRUCT_FMT = '''\
/**
 * Message {proto_name} in package {package}.
 */
{repeated_struct}

struct {namespace}_{name}_t {{
    struct pbtools_message_base_t base;
{members}
}};
'''

MESSAGE_DECLARATION_FMT = '''\
/**
 * Create a new message {proto_name} in given workspace.
 *
 * @param[in] workspace_p Message workspace.
 * @param[in] size Workspace size.
 *
 * @return Initialized address book, or NULL on failure.
 */
struct {namespace}_{name}_t *{namespace}_{name}_new(
    void *workspace_p,
    size_t size);

/**
 * Encode message {proto_name} defined in package {package}.
 *
 * @param[in] self_p Message to encode.
 * @param[out] encoded_p Buffer to encode the message into.
 * @param[in] size Encoded buffer size.
 *
 * @return Encoded data length or negative error code.
 */
int {namespace}_{name}_encode(
    struct {namespace}_{name}_t *self_p,
    uint8_t *encoded_p,
    size_t size);

/**
 * Decode message {proto_name} defined in package {package}.
 *
 * @param[in,out] self_p Initialized message to decode into.
 * @param[in] encoded_p Buffer to decode.
 * @param[in] size Size of the encoded message.
 *
 * @return Number of bytes decoded or negative error code.
 */
int {namespace}_{name}_decode(
    struct {namespace}_{name}_t *self_p,
    const uint8_t *encoded_p,
    size_t size);
'''

MESSAGE_STATIC_DECLARATIONS_FMT = '''\
static void {namespace}_{name}_init(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_heap_t *heap_p,
    struct {namespace}_{name}_t *next_p);

static void {namespace}_{name}_encode_inner(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_encoder_t *encoder_p);

static void {namespace}_{name}_decode_inner(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_decoder_t *decoder_p);
'''

MESSAGE_STATIC_DEFINITIONS_FMT = '''\
static void {namespace}_{name}_init(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_heap_t *heap_p,
    struct {namespace}_{name}_t *next_p)
{{
    self_p->base.heap_p = heap_p;
    self_p->base.next_p = &next_p->base;
{members_init}
}}

static void {namespace}_{name}_encode_inner(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_encoder_t *encoder_p)
{{
{encode_body}\
}}

static void {namespace}_{name}_decode_inner(
    struct {namespace}_{name}_t *self_p,
    struct pbtools_decoder_t *decoder_p)
{{
    int wire_type;

    while (pbtools_decoder_available(decoder_p)) {{
        switch (pbtools_decoder_read_tag(decoder_p, &wire_type)) {{

{decode_body}
        default:
            pbtools_decoder_skip_field(decoder_p, wire_type);
            break;
        }}
    }}
{finalizers}\
}}
'''

ENCODE_INNER_MEMBER_FMT = '''\
    pbtools_encoder_write_{type}(encoder_p, {field_number}, {ref}self_p->{name});
'''

ENCODE_INNER_REPEATED_MEMBER_FMT = '''\
    pbtools_encoder_write_repeated_{type}(encoder_p, {field_number}, &self_p->{name});
'''

ENCODE_INNER_MESSAGE_MEMBER_FMT = '''\
    {namespace}_{name}_encode_inner(encoder_p, {field_number}, &self_p->{field_name});
'''

ENCODE_INNER_REPEATED_MESSAGE_MEMBER_FMT = '''\
    {namespace}_{name}_encode_repeated_inner(
        encoder_p,
        {field_number},
        &self_p->{field_name});
'''

DECODE_INNER_MEMBER_FMT = '''\
        case {field_number}:
            self_p->{name} = pbtools_decoder_read_{type}(decoder_p, wire_type);
            break;
'''

DECODE_INNER_MEMBER_BYTES_AND_STRING_FMT = '''\
        case {field_number}:
            pbtools_decoder_read_{type}(decoder_p, wire_type, &self_p->{name});
            break;
'''

DECODE_INNER_REPEATED_MEMBER_FMT = '''\
        case {field_number}:
            pbtools_decoder_read_repeated_{type}(
                decoder_p,
                wire_type,
                &self_p->{name});
            break;
'''

DECODE_INNER_REPEATED_MESSAGE_MEMBER_FMT = '''\
        case {field_number}:
            {namespace}_{name}_decode_repeated_inner(
                decoder_p,
                wire_type,
                &self_p->{field_name});
            break;
'''

MESSAGE_DEFINITION_FMT = '''\
{repeated}\
struct {namespace}_{name}_t *{namespace}_{name}_new(
    void *workspace_p,
    size_t size)
{{
    return (pbtools_message_new(workspace_p,
                                size,
                                sizeof(struct {namespace}_{name}_t),
                                (pbtools_message_init_t){namespace}_{name}_init));
}}

int {namespace}_{name}_encode(
    struct {namespace}_{name}_t *self_p,
    uint8_t *encoded_p,
    size_t size)
{{
    return (pbtools_message_encode(
        &self_p->base,
        encoded_p,
        size,
        (pbtools_message_encode_inner_t){namespace}_{name}_encode_inner));
}}

int {namespace}_{name}_decode(
    struct {namespace}_{name}_t *self_p,
    const uint8_t *encoded_p,
    size_t size)
{{
    return (pbtools_message_decode(
        &self_p->base,
        encoded_p,
        size,
        (pbtools_message_decode_inner_t){namespace}_{name}_decode_inner));
}}
'''

REPEATED_STRUCT_FMT = '''\
struct {namespace}_{name}_repeated_t {{
    int length;
    struct {namespace}_{name}_t **items_pp;
    struct {namespace}_{name}_t *head_p;
    struct {namespace}_{name}_t *tail_p;
}};\
'''

REPEATED_DECLARATION_FMT = '''\
int {namespace}_{name}_{field_name}_alloc(
    struct {namespace}_{name}_t *self_p,
    int length);
'''

REPEATED_DEFINITION_FMT = '''\
int {namespace}_{name}_{field_name}_alloc(
    struct {namespace}_{name}_t *self_p,
    int length)
{{
    return (pbtools_alloc_repeated_{type}(
        &self_p->{field_name},
        self_p->base.heap_p,
        length));
}}
'''

REPEATED_MESSAGE_DEFINITION_FMT = '''\
int {namespace}_{name}_{field_name}_alloc(
    struct {namespace}_{name}_t *self_p,
    int length)
{{
    int res;
    int i;
    struct {namespace}_{name}_t *items_p;

    res = -1;
    self_p->{field_name}.items_pp = pbtools_heap_alloc(
        self_p->base.heap_p,
        sizeof(items_p) * length);

    if (self_p->{field_name}.items_pp != NULL) {{
        items_p = pbtools_heap_alloc(self_p->base.heap_p, sizeof(*items_p) * length);

        if (items_p != NULL) {{
            for (i = 0; i < length; i++) {{
                {namespace}_{name}_init(
                    &items_p[i],
                    self_p->base.heap_p,
                    &items_p[i + 1]);
                self_p->{field_name}.items_pp[i] = &items_p[i];
            }}

            items_p[length - 1].base.next_p = NULL;
            self_p->{field_name}.length = length;
            self_p->{field_name}.head_p = &items_p[0];
            self_p->{field_name}.tail_p = &items_p[length - 1];
            res = 0;
        }}
    }}

    return (res);
}}
'''

REPEATED_MESSAGE_STATIC_DECLARATIONS_FMT = '''\
static void {namespace}_{name}_encode_repeated_inner(
    struct pbtools_encoder_t *encoder_p,
    int field_number,
    struct {namespace}_{name}_repeated_t *repeated_p);

static void {namespace}_{name}_decode_repeated_inner(
    struct pbtools_decoder_t *decoder_p,
    int wire_type,
    struct {namespace}_{name}_repeated_t *repeated_p);

static void {namespace}_{name}_finalize_repeated_inner(
    struct pbtools_decoder_t *decoder_p,
    struct {namespace}_{name}_repeated_t *repeated_p);
'''

REPEATED_MESSAGE_STATIC_DEFINITIONS_FMT = '''\
static void {namespace}_{name}_encode_repeated_inner(
    struct pbtools_encoder_t *encoder_p,
    int field_number,
    struct {namespace}_{name}_repeated_t *repeated_p)
{{
    int i;
    int pos;

    for (i = repeated_p->length - 1; i >= 0; i--) {{
        pos = encoder_p->pos;
        {namespace}_{name}_encode_inner(repeated_p->items_pp[i], encoder_p);
        pbtools_encoder_write_length_delimited(encoder_p,
                                               field_number,
                                               pos - encoder_p->pos);
    }}
}}

static void {namespace}_{name}_decode_repeated_inner(
    struct pbtools_decoder_t *decoder_p,
    int wire_type,
    struct {namespace}_{name}_repeated_t *repeated_p)
{{
    size_t size;
    struct pbtools_decoder_t decoder;
    struct {namespace}_{name}_t *item_p;

    if (wire_type != PBTOOLS_WIRE_TYPE_LENGTH_DELIMITED) {{
        pbtools_decoder_abort(decoder_p, PBTOOLS_BAD_WIRE_TYPE);

        return;
    }}

    item_p = pbtools_decoder_heap_alloc(decoder_p, sizeof(*item_p));

    if (item_p == NULL) {{
        return;
    }}

    size = pbtools_decoder_read_varint(decoder_p);
    {namespace}_{name}_init(item_p, decoder_p->heap_p, NULL);
    pbtools_decoder_init_slice(&decoder, decoder_p, size);
    {namespace}_{name}_decode_inner(item_p, &decoder);
    pbtools_decoder_seek(decoder_p, pbtools_decoder_get_result(&decoder));
    item_p->base.next_p = NULL;

    if (repeated_p->length == 0) {{
        repeated_p->head_p = item_p;
    }} else {{
        repeated_p->tail_p->base.next_p = &item_p->base;
    }}

    repeated_p->tail_p = item_p;
    repeated_p->length++;
}}

static void {namespace}_{name}_finalize_repeated_inner(
    struct pbtools_decoder_t *decoder_p,
    struct {namespace}_{name}_repeated_t *repeated_p)
{{
    int i;
    struct {namespace}_{name}_t *item_p;

    if (repeated_p->length == 0) {{
        return;
    }}

    repeated_p->items_pp = pbtools_decoder_heap_alloc(
        decoder_p,
        sizeof(item_p) * repeated_p->length);

    if (repeated_p->items_pp == NULL) {{
        return;
    }}

    item_p = repeated_p->head_p;

    for (i = 0; i < repeated_p->length; i++) {{
        repeated_p->items_pp[i] = item_p;
        item_p = (struct {namespace}_{name}_t *)item_p->base.next_p;
    }}
}}
'''

REPEATED_FINALIZER_FMT = '''\
    pbtools_decoder_finalize_repeated_{type}(
        decoder_p,
        &self_p->{field_name});\
'''

REPEATED_MESSAGE_FINALIZER_FMT = '''\
    {namespace}_{name}_finalize_repeated_inner(
        decoder_p,
        &self_p->{field_name});\
'''

ENUM_FMT = '''\
/**
 * Enum {proto_name} in package {package}.
 */
enum {namespace}_{name}_e {{
{members}
}};
'''

ENUM_MEMBER_FMT = '''\
    {namespace}_{name}_{field_name}_e = {field_number}\
'''


def canonical(value):
    """Replace anything but 'a-z', 'A-Z' and '0-9' with '_'.

    """

    return re.sub(r'[^a-zA-Z0-9]', '_', value)


def camel_to_snake_case(value):
    value = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', value)
    value = re.sub(r'(_+)', '_', value)
    value = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', value).lower()
    value = canonical(value)

    return value


def generate_struct_member_fmt(type, name):
    if type in ['int32', 'int64', 'uint32', 'uint64']:
        type = f'{type}_t'
    elif type in ['sint32', 'sint64']:
        type = f'{type[1:]}_t'
    elif type in ['fixed32', 'fixed64']:
        type = f'uint{type[5:]}_t'
    elif type in ['sfixed32', 'sfixed64']:
        type = f'int{type[6:]}_t'
    elif type in ['float', 'double', 'bool']:
        pass
    elif type in ['bytes', 'string']:
        type = f'struct pbtools_bytes_t'
    else:
        type = f'{camel_to_snake_case(type)}_t'

    return f'    {type} {name};'


def generate_repeated_struct_member_fmt(namespace, type, name):
    if type in PRIMITIVE_TYPES:
        if type in ['sint32', 'sint64']:
            type = type[1:]
        elif type in ['fixed32', 'fixed64']:
            type = f'uint{type[5:]}'
        elif type in ['sfixed32', 'sfixed64']:
            type = f'int{type[6:]}'

        type = f'struct pbtools_repeated_{type}_t'
    else:
        type = f'struct {namespace}_{camel_to_snake_case(type)}_repeated_t'

    return f'    {type} {name};'


def generate_struct_members(namespace, message):
    members = []

    for field in message.fields:
        if field.repeated:
            members.append(
                generate_repeated_struct_member_fmt(namespace,
                                                    field.type,
                                                    field.name))
        else:
            members.append(generate_struct_member_fmt(field.type,
                                                      field.name))

    return members


def generate_repeated_struct(namespace, message):
    return REPEATED_STRUCT_FMT.format(namespace=namespace,
                                      name=camel_to_snake_case(message.name))


def generate_enum_members(namespace, enum):
    members = []

    for field in enum.fields:
        members.append(
            ENUM_MEMBER_FMT.format(namespace=namespace,
                                   name=camel_to_snake_case(enum.name),
                                   field_name=camel_to_snake_case(field.name),
                                   field_number=field.field_number))

    return ',\n'.join(members)


def generate_structs(namespace, parsed):
    structs = []

    for enum in parsed.enums:
        members = generate_enum_members(namespace, enum)
        structs.append(ENUM_FMT.format(namespace=namespace,
                                       package=parsed.package,
                                       proto_name=enum.name,
                                       name=camel_to_snake_case(enum.name),
                                       members=members))

    for message in parsed.messages:
        repeated_struct = generate_repeated_struct(namespace, message)
        members = generate_struct_members(namespace, message)
        structs.append(
            MESSAGE_STRUCT_FMT.format(namespace=namespace,
                                      package=parsed.package,
                                      proto_name=message.name,
                                      name=camel_to_snake_case(message.name),
                                      repeated_struct=repeated_struct,
                                      members='\n'.join(members)))

    return '\n'.join(structs)


def generate_declarations(namespace, parsed):
    declarations = []

    for message in parsed.messages:
        message_name = camel_to_snake_case(message.name)

        for field in message.repeated_fields:
            declarations.append(
                REPEATED_DECLARATION_FMT.format(namespace=namespace,
                                                name=message_name,
                                                field_name=field.name))

        declarations.append(
            MESSAGE_DECLARATION_FMT.format(namespace=namespace,
                                           package=parsed.package,
                                           proto_name=message.name,
                                           name=message_name))

    return '\n'.join(declarations)


def generate_message_encode_body(namespace, message):
    members = []
    message_name = camel_to_snake_case(message.name)

    for field in reversed(message.fields):
        if field.type in PRIMITIVE_TYPES:
            if field.repeated:
                members.append(
                    ENCODE_INNER_REPEATED_MEMBER_FMT.format(
                        type=field.type,
                        field_number=field.field_number,
                        name=field.name))
            else:
                if field.type in ['bytes', 'string']:
                    ref = '&'
                else:
                    ref = ''

                members.append(
                    ENCODE_INNER_MEMBER_FMT.format(
                        type=field.type,
                        field_number=field.field_number,
                        name=field.name,
                        ref=ref))
        else:
            if field.repeated:
                members.append(
                    ENCODE_INNER_REPEATED_MESSAGE_MEMBER_FMT.format(
                        namespace=namespace,
                        name=message_name,
                        field_number=field.field_number,
                        field_name=field.name))
            else:
                members.append(
                    ENCODE_INNER_MESSAGE_MEMBER_FMT.format(
                        namespace=namespace,
                        name=message_name,
                        field_number=field.field_number,
                        field_name=field.name))


    return ''.join(members)


def generate_repeated_field_decode_body(namespace, message, field):
    if field.type in PRIMITIVE_TYPES:
        return DECODE_INNER_REPEATED_MEMBER_FMT.format(
            type=field.type,
            field_number=field.field_number,
            name=field.name)
    else:
        return DECODE_INNER_REPEATED_MESSAGE_MEMBER_FMT.format(
            namespace=namespace,
            name=camel_to_snake_case(message.name),
            field_number=field.field_number,
            field_name=field.name)


def generate_message_decode_body(namespace, message):
    members = []

    for field in message.fields:
        if field.repeated:
            members.append(generate_repeated_field_decode_body(namespace,
                                                               message,
                                                               field))
        elif field.type in ['bytes', 'string']:
            members.append(
                DECODE_INNER_MEMBER_BYTES_AND_STRING_FMT.format(
                    type=field.type,
                    field_number=field.field_number,
                    name=field.name))
        elif field.type in PRIMITIVE_TYPES:
            members.append(
                DECODE_INNER_MEMBER_FMT.format(field_number=field.field_number,
                                               type=field.type,
                                               name=field.name))

    return '\n'.join(members)


def generate_message_members_init(message):
    members = []

    for field in message.fields:
        name = field.name

        if field.repeated:
            members.append(f'    self_p->{name}.length = 0;')
        elif field.type in ['bytes', 'string']:
            members.append(f'    pbtools_{field.type}_init(&self_p->{name});')
        elif field.type in PRIMITIVE_TYPES:
            members.append(f'    self_p->{name} = 0;')

    return '\n'.join(members)


def generate_repeated_definitions(namespace, message):
    members = []
    message_name = camel_to_snake_case(message.name)

    for field in message.repeated_fields:
        if field.type in PRIMITIVE_TYPES:
            members.append(
                REPEATED_DEFINITION_FMT.format(namespace=namespace,
                                               name=message_name,
                                               field_name=field.name,
                                               type=field.type))
        else:
            members.append(
                REPEATED_MESSAGE_DEFINITION_FMT.format(namespace=namespace,
                                                       name=message_name,
                                                       field_name=field.name,
                                                       type=field.type))
            members.append(
                REPEATED_MESSAGE_STATIC_DEFINITIONS_FMT.format(
                    namespace=namespace,
                    name=message_name,
                    field_name=field.name,
                    type=field.type))

    if members:
        members.append('')

    return '\n'.join(members)


def generate_repeated_finalizers(namespace, message):
    finalizers = []
    message_name = camel_to_snake_case(message.name)

    for field in message.repeated_fields:
        if field.type in PRIMITIVE_TYPES:
            finalizers.append(
                REPEATED_FINALIZER_FMT.format(namespace=namespace,
                                              field_name=field.name,
                                              type=field.type))
        else:
            finalizers.append(
                REPEATED_MESSAGE_FINALIZER_FMT.format(namespace=namespace,
                                                      name=message_name,
                                                      field_name=field.name))

    if finalizers:
        finalizers = [''] + finalizers + ['']

    return '\n'.join(finalizers)


def generate_definitions(namespace, parsed):
    definitions = []

    for message in parsed.messages:
        message_name = camel_to_snake_case(message.name)
        definitions.append(
            MESSAGE_STATIC_DECLARATIONS_FMT.format(
                namespace=namespace,
                name=message_name))

        for field in message.repeated_fields:
            if field.type in PRIMITIVE_TYPES:
                continue

            definitions.append(
                REPEATED_MESSAGE_STATIC_DECLARATIONS_FMT.format(
                    namespace=namespace,
                    name=message_name))

    for message in parsed.messages:
        encode_body = generate_message_encode_body(namespace, message)
        decode_body = generate_message_decode_body(namespace, message)
        members_init = generate_message_members_init(message)
        repeated = generate_repeated_definitions(namespace, message)
        finalizers = generate_repeated_finalizers(namespace, message)
        definitions.append(
            MESSAGE_STATIC_DEFINITIONS_FMT.format(
                namespace=namespace,
                name=camel_to_snake_case(message.name),
                encode_body=encode_body,
                decode_body=decode_body,
                members_init=members_init,
                finalizers=finalizers))
        definitions.append(
            MESSAGE_DEFINITION_FMT.format(namespace=namespace,
                                          package=parsed.package,
                                          proto_name=message.name,
                                          name=camel_to_snake_case(message.name),
                                          repeated=repeated))

    return '\n'.join(definitions)


def generate(namespace, parsed, header_name):
    """Generate C source code from given parsed proto-file.

    """

    namespace = camel_to_snake_case(parsed.package)
    namespace_upper = namespace.upper()
    include_guard = '{}_H'.format(namespace_upper)

    structs = generate_structs(namespace, parsed)
    declarations = generate_declarations(namespace, parsed)
    definitions = generate_definitions(namespace, parsed)

    header = HEADER_FMT.format(namespace=namespace,
                               namespace_upper=namespace.upper(),
                               include_guard=include_guard,
                               structs=structs,
                               declarations=declarations)

    source = SOURCE_FMT.format(namespace=namespace,
                               namespace_upper=namespace.upper(),
                               header=header_name,
                               definitions=definitions)

    return header, source
