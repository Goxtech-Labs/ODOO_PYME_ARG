# Motor documental ARG — implementación

Compatibilidad: Odoo 20 Community. La versión de cada addon está fijada en la
[composición de esta entrega](../../composition/versions.lock.json); consultar sus límites y estado de QA.

arg_pyme_documentos 20.0.1.0.5 depende de Base/UI/web. Mixin abstracto arg.pyme.document.mixin; no tabla operativa universal. Los circuitos heredan sus modelos nativos y el mixin, devuelven código desde _arg_document_code y declaran ACL propias.
arg_identity_id apunta exclusivamente al registro Base; arg_document_type_id y arg_number son relacionados de lectura. Create asigna después del guardado nativo; identidad/compañía quedan protegidas y unlink exige cancelación/reversión. No confiar en flags de contexto recibidos por RPC.

_arg_axis clasifica cada línea elegible con su precisión, sin sumar unidades incompatibles: target,done,pending,closed,state. El eje usa la misma precisión y distingue faltante cerrado. _arg_get_completion_axes debe calcular desde fuentes reales; cada adaptador amplía depends de _compute_arg_completion_axes para invalidar al cambiar sus fuentes. Nunca escribir residuales o existencias para conseguir un indicador.

_arg_document_relations devuelve recordsets con vínculos reales; _arg_document_line_relations devuelve referencias ORM de documento/línea origen/destino, cantidad y unidad. arg_document_links comprueba ACL y compañías de cada referencia antes de devolver metadatos. Widget arg_document_header y acción arg_pyme.document_links usan APIs nativas.

_arg_report_payload debe aportar snapshot histórico y valores formateados: title,date,state_label,partner_name,partner_address,external_reference,lines(description,quantity,unit,unit_price,total),currency,totals(label,amount),notes. Adaptador ausente rechaza impresión; no inventa contenido. Identidad/compañía/borrador/ejemplo provienen del servidor y no del data enviado por navegador.

La acción genérica transmite arg_model y arg_ids: en Odoo20 un reporte con data no vacío omite docids de la URL. El modelo de reporte valida IDs, modelo concreto habilitado, usuario interno, rol ARG, ACL y compañía, sin sudo. No incorpora CAE ficticio ni reemplaza reporte fiscal autorizado.
Sin adaptadores comerciales en este addon para evitar dependencias inversas. Los adaptadores de PRE/PED residen en Ventas y los demás en sus circuitos instalados; se conserva la dependencia hacia Documentos. Escenarios quickstart reservados para QA posterior.

Versión20.0.1.0.3: arg_demo se fija desde compañía al crear y queda inmutable; marca Ejemplo no desaparece por cambiar ajustes posteriores. Reporte respeta snapshot de compañía. Vínculos sin cantidad atribuible muestran Sin desglosar.

Actualización en entrega007: ver [registro](../entregas/007-compras.md). Defaults RPC protegidos y composición de adaptadores.
