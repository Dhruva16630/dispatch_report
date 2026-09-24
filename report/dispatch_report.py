from odoo import fields, models, tools


class DispatchReport(models.Model):
    _name = "dispatch.report"
    _description = "Dispatch Report"
    _auto = False

    product_id = fields.Many2one(
        "product.product",
        string="Product",
        readonly=True,
    )

    quantity_delivered = fields.Float(
        string="Quantity Delivered",
        readonly=True,
    )

    total_demand = fields.Float(
        string="Total Demand",
        readonly=True,
    )

    quantity_to_deliver = fields.Float(
        string="Quantity to Deliver",
        readonly=True,
    )

    uom = fields.Many2one(
        "uom.uom",
        string="UoM",
        readonly=True,
    )
    
    hsn_code = fields.Char(
        string="HSN Code",
        readonly = True
    )

    barcode = fields.Char(
        string="Barcode",
        readonly=True,
    )

    fiscal_position = fields.Many2one(
        "account.fiscal.position",
        string="Fiscal Position",
        readonly=True,
    )

    payment_terms = fields.Many2one(
        "account.payment.term",
        string="Payment Terms",
        readonly=True,
    )

    internal_reference = fields.Char(
        string="Internal Reference",
        readonly=True,
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Date",
        readonly=True,
    )

    def init(self):
        tools.drop_view_if_exists(
            self.env.cr,
            self._table,
        )

        self.env.cr.execute("""
            CREATE VIEW dispatch_report AS (

                SELECT
                    sm.id AS id,

                    sm.product_id AS product_id,

                    sm.quantity AS quantity_delivered,

                    sm.product_uom_qty AS total_demand,

                    sm.product_uom_qty - sm.quantity
                        AS quantity_to_deliver,

                    sm.product_uom AS uom,
                    
                    pt.l10n_in_hsn_code AS hsn_code,

                    pp.barcode AS barcode,

                    so.fiscal_position_id AS fiscal_position,

                    so.payment_term_id AS payment_terms,

                    pp.default_code AS internal_reference,

                    sm.date AS scheduled_date

                FROM stock_move sm

                JOIN product_product pp
                    ON pp.id = sm.product_id

                JOIN product_template pt
                    ON pt.id = pp.product_tmpl_id

                LEFT JOIN stock_picking sp
                    ON sp.id = sm.picking_id

                LEFT JOIN sale_order so
                    ON so.id = sp.sale_id
            )
        """)