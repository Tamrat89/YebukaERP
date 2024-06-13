
from odoo import models, fields, api, _


class ManagerPerformanceAmibara(models.Model):
    _name = 'manager.performance.amibara'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference")
    employee_id = fields.Many2one('hr.employee', string="የኃላፊው ስም", tracking=True, required=True )
    company_id = fields.Many2one('res.company', related="employee_id.company_id")
    department_id = fields.Many2one('hr.department', string="የሚሠራበት ክፍል", related="employee_id.department_id")
    job_title = fields.Many2one('hr.job', related="employee_id.job_id", string="የሥራ መደብ")
    evalutator_name = fields.Many2one('hr.employee', string="የገምጋሚው ኃላፊ ስም")
    evalutator_name2 = fields.Many2one('hr.employee', string="የበላይ ኃላፊው ስም")
    evaluate_round = fields.Selection([
        ('round1', 'Round 1'),
        ('round2 ', 'Round 2'),
    ], string='የምዘና ዙር')

    date_hired_p = fields.Date( string="ግምገማዉ የጀመረበት ቀን", compute="_compute_date_start", required=True, default=fields.Date.today)
    last_evaulation_date = fields.Date(string="ግምገማዉ ያለቀበት ቀን", required=True, default=fields.Date.today)
    evaluation_date = fields.Date(string="የምዘናው ቀን", required=True, default=fields.Date.today)
    evaluation_period_from = fields.Date(string="የምዘናው ወቅት ከ")
    evaluation_period_to = fields.Date(string="እስከ")
    general_comment = fields.Text(string="ተገምጋሚው በሥራ አፈፃፀሙ የተገኙበት ዋና ዋና ድክመቶች፡-")
    general_comment1 = fields.Text(string="ተገምጋሚው የሚያስመሰግኑት ዋና ዋና ተግባራት፡-")
    # general_comment2 = fields.Text(string="ሠራተኛዉ ያሳየዉ ድክመት ካለ የምወሰድ እርምጃ")
    date_of_manager_evaluate = fields.Date(string="ቀን", required=True, default=fields.Date.today)
    employee_comment = fields.Text(string="ተገምጋሚው ስለግምገማው ያለው አስተያየት፡-")
    general_comment4 = fields.Text(string="የገምጋሚው ኃላፊ የበላይ ኃላፊ አስተያየት")



    date = fields.Date(string="Date", required=True, default=fields.Date.today)

    # employee_comment = fields.Text(string="Employee Comment")
    performance_line_ids = fields.One2many('performance.line.amibara.manager','performance_id',string="Performances", )

    state = fields.Selection([('draft','Draft'),('submit','Submit'),('approve','Approved'),('validate','Validated')], default='draft')

    total_value = fields.Integer(compute='_compute_total_value', string="ድምር ዉጤት")
    total_performance_value_divided = fields.Float(compute='_compute_total_performance_value_divided', string="አማካይ የግምገማ ዉጤት")
    total_value_percent = fields.Float(compute='_compute_total_value_percent', string="Total Value (%)")
    total_performance_value_divided_percent = fields.Float(compute='_compute_total_performance_value_divided_percent', string="Total Performance Value Divided (%)")

    @api.depends('total_performance_value_divided')
    def _compute_total_performance_value_divided_percent(self):
        for performance in self:
            performance.total_performance_value_divided_percent = performance.total_performance_value_divided * 100

    # @api.depends('total_value')
    # def _compute_total_value_percent(self):
    #     for performance in self:
    #         if performance.total_value:
    #             percent = (performance.total_value / 22) * 100
    #             performance.total_value_percent = min(percent, 100)  # Ensure percent does not exceed 100
    #         else:
    #             performance.total_value_percent = 0.0

    @api.model
    def _compute_total_value(self):
        for performance in self:
            total_value = sum(line.total_value for line in performance.performance_line_ids)
            performance.total_value = total_value

    @api.depends('total_value')
    def _compute_total_performance_value_divided(self):
        for performance in self:
            if performance.total_value:
                performance.total_performance_value_divided = performance.total_value / 22
            else:
                performance.total_performance_value_divided = 0.0
    @api.depends('employee_id')
    def _compute_date_start(self):
        for rec in self:
            date_hire = self.env['hr.contract'].search(['&',('employee_id','=',rec.employee_id.id),('state','=','running')])
            rec.date_hired_p = date_hire.date_start

    def action_submit(self):
        self.state = 'submit'

    def action_approve(self):
        self.state = 'approve'

class PerformanceLineAmibaraManager(models.Model):
    _name = "performance.line.amibara.manager"

    criteria_id = fields.Many2one('manager_competency.criteria', string="መሥፈርት")
    criteria_description = fields.Text(compute="_compute_criteria_description", string='Description')
    performance_id = fields.Many2one('manager.performance.amibara', ondelete='cascade', index=True, copy=False)
    ff = fields.Boolean(string="እ.በ.ጥሩ(5)")
    ee = fields.Boolean(string="በጣም ጥሩ(4)")
    me = fields.Boolean(string="አጥጋቢ(3)")
    ni = fields.Boolean(string="ሊሻሻል የሚገባው(2)")
    a = fields.Boolean(string="ዝቅተኛ(1)")

    # remark = fields.Text(string="Remark For Improvement")
    total_value = fields.Integer(compute="_compute_total_value", string="Total Value")

    total_performance_value = fields.Integer(compute='_compute_total_performance_value', string="Total Performance Value")
    total_performance_value_divided = fields.Float(compute='_compute_total_performance_value_divided', string="Total Performance Value Divided")

    @api.depends('total_performance_value')
    def _compute_total_performance_value_divided(self):
        for performance in self:
            if performance.total_performance_value:
                performance.total_performance_value_divided = performance.total_performance_value / 22
            else:
                performance.total_performance_value_divided = 0.0

    @api.depends('performance_id.performance_line_ids.total_value')
    def _compute_total_performance_value(self):
        for performance in self:
            total_value = sum(line.total_value for line in performance.performance_id.performance_line_ids)
            performance.total_performance_value = total_value

    # Existing methods







    @api.depends('criteria_id')
    def _compute_criteria_description(self):
        for record in self:
            record.criteria_description = record.criteria_id.description or ''

    @api.depends('ff','ee', 'me', 'ni','a')
    def _compute_total_value(self):
        for record in self:
            total_value = 0
            if record.ff:
                total_value += 5
            if record.ee:
                total_value += 4
            if record.me:
                total_value += 3
            if record.ni:
                total_value += 2
            if record.a:
                total_value += 1
            record.total_value = total_value

    def _update_total_values(self):
        records = self.search([])
        for record in records:
            record._compute_total_value()


    @api.model
    def create(self, vals):
        record = super(PerformanceLineAmibaraManager, self).create(vals)
        record.performance_id._compute_total_value()
        return record

    def write(self, vals):
        res = super(PerformanceLineAmibaraManager, self).write(vals)
        self.performance_id._compute_total_value()
        return res


class CompetencyCriteriaManager(models.Model):
    _name = 'manager_competency.criteria'

    name = fields.Char(string='Title')
    remark = fields.Text(string="Remark")

