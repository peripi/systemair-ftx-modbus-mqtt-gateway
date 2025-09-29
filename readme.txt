

periodically check ftx through modbus queries.

modbus queries based on list of ftx-registers. For every register publish on mqtt if "active"

if recived mqtt/order
    match against registers, send value to ftx through modbus

fxt /
 /air flow/set
 /temperature
 /etc


if