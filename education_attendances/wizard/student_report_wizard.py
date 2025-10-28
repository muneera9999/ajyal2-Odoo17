from odoo import models, fields

class StudentReport(models.TransientModel):
    _name = 'student.report.wizard'
    _description = 'Student Attendance Report'

    academic_year_id = fields.Many2one('education.academic.year',
                                       string='Academic Year',  required=True)
    admission_class_id = fields.Many2many('education.class', string='Class', required=True)

    def action_print_xlsx(self):
        students = self.env['education.student'].search([
            ('academic_year_id', '=', self.academic_year_id.id) ])
            # ('admission_class_id', 'in', self.admission_class_id.ids),
        
        if hasattr(students, 'admission_class_id'):
                selected_class_ids = self.admission_class_id.ids
                students = students.filtered(
                lambda student: any(
                class_id.id in selected_class_ids
                for class_id in student.admission_class_id
            ))

        
        student_ids = ','.join(str(id) for id in students.ids)
        return {
            # 'type': 'ir.actions.act_window',
            'type': 'ir.actions.act_url',
            # 'res_model': 'student.report.wizard',
            'url': f'/student/excel/report/{student_ids}',
            ## 'view_mode': 'form',
            'target': 'new',
        }
