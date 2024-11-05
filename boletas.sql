CREATE TABLE boletas ( folio VARCHAR(50) PRIMARY KEY, -- Identificador del folio, ajusta el tamaño si es necesario
 fecha DATE, -- Fecha de emisión
 rut_razon_emisor VARCHAR(20), -- RUT del emisor (identificación fiscal)
 nombre_razon_emisor VARCHAR(100), -- Nombre de la razón social del emisor
 na VARCHAR(50), -- Campo NA, ajustar tamaño si es necesario
 direccion VARCHAR(150), -- Dirección
 comuna VARCHAR(50), -- Comuna
 neto NUMERIC(15, 2), -- Valor neto
 iva NUMERIC(15, 2), -- Valor del IVA
 bruto NUMERIC(15, 2), -- Valor bruto (neto + IVA)
 cruce_ted NUMERIC(15, 2), -- Valor cruzado del archivo TED
 descuento NUMERIC(15, 2), -- Descuento calculado
 nombre_local VARCHAR(100) -- Nombre del local asociado
);

