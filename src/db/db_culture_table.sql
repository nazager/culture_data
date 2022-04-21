CREATE TABLE IF NOT EXISTS cultura (
    "Cod_Loc" numeric NOT NULL,
    "IdProvincia" numeric NOT NULL,
    "IdDepartamento" numeric NOT NULL,
    "Categoría" text NOT NULL,
    "Provincia" text,
    "Localidad" text,
    "Nombre" text,
    "Dirección" text,
    "CP" text,
    "Teléfono" text,
    "Mail" text,
    "Web" text,
    "Fecha_de_carga" date
);