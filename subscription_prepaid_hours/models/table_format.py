# -*- coding: utf-8 -*-
# © 2016 ClearCorp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

APP_ID = """"
<group>
    <div style="padding-bottom:16px">
        <h2 style="display:inline; margin-right:24px">Approval</h2>
            <span>
                Estado
                <button style="margin-left:16px"
                    name="do_approve_approval" string="Approve" type="object"
                    context="{'approval_id':"""

PREPAID_NAME = """}"/>
            </span>
        </div>
        <br/>
        <table style="width:100%">
            <thead>
                <tr>
                    <th style="width:25%"></th>
                    """

PREPAID_TIME = """
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Horas Bolsa</td>"""

FOOTER = """
                        </ul>
                    </td>
                </tr>
            </tbody>
        </table>
    </group><br/>"""

COMPLETE_TABLE = """
<group>
    <div style="padding-bottom:16px">
        <h2 style="display:inline; margin-right:24px">Approval</h2>
        <span>
            Estado
            <button style="margin-left:16px"
                name="_approve_approval" string="Approve"
                context="{'approval_id': 1}"/>
        </span>
    </div>
    <table>
        <thead>
            <tr>
                <th></th>
                <th style="text-align:right">%s</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Horas Bolsa</td>
                <td style="text-align:right">%s</td>
            </tr>
            <tr>
                <td>Horas Consumidas</td>
                <td style="text-align:right">-</td>
            </tr>
            <tr style="border-top:1px solid black">
                <td style="padding-bottom:16px">
                    <b>Horas Restantes</b>
                </td>
                <td style="text-align:right">
                    <b>-</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas por aprobar</b>
                </td>
                <td style="text-align:right">
                    <b>SUMA DE OTROS APPROVALS</b>
                </td>
            </tr>
            <tr>
                <td>
                    <b>Horas requeridas</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
                <td style="text-align:right">
                    <b>SUMA</b>
                    <ul style="list-style-type:none">
                        <li>%s</li>
                    </ul>
                </td>
            </tr>
        </tbody>
    </table>
</group>"""