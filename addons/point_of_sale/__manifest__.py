# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

{
    'name': 'Point of Sale',
    'version': '1.0.1',
    'category': 'Sales/Point of Sale',
    'sequence': 40,
    'summary': 'User-friendly PoS interface for shops and restaurants',
    'description': "",
    'depends': ['stock_account', 'barcodes', 'web_editor', 'digest'],
    'data': [
        'security/point_of_sale_security.xml',
        'security/ir.model.access.csv',
        'data/default_barcode_patterns.xml',
        'data/digest_data.xml',
        'wizard/pos_box.xml',
        'wizard/pos_details.xml',
        'wizard/pos_payment.xml',
        'views/pos_assets_common.xml',
        'views/pos_assets_index.xml',
        'views/pos_assets_qunit.xml',
        'views/point_of_sale_report.xml',
        'views/point_of_sale_view.xml',
        'views/pos_order_view.xml',
        'views/pos_category_view.xml',
        'views/product_view.xml',
        'views/account_journal_view.xml',
        'views/pos_payment_method_views.xml',
        'views/pos_payment_views.xml',
        'views/pos_config_view.xml',
        'views/pos_session_view.xml',
        'views/point_of_sale_sequence.xml',
        'views/customer_facing_display.xml',
        'data/point_of_sale_data.xml',
        'views/pos_order_report_view.xml',
        'views/account_statement_view.xml',
        'views/res_config_settings_views.xml',
        'views/digest_views.xml',
        'views/res_partner_view.xml',
        'views/report_userlabel.xml',
        'views/report_saledetails.xml',
        'views/point_of_sale_dashboard.xml',
    ],
    'demo': [
        'data/point_of_sale_demo.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
        'static/src/xml/Chrome.xml',
        'static/src/xml/debug_manager.xml',
        'static/src/xml/Screens/ProductScreen/ProductScreen.xml',
        'static/src/xml/Screens/ClientListScreen/ClientLine.xml',
        'static/src/xml/Screens/ClientListScreen/ClientDetailsEdit.xml',
        'static/src/xml/Screens/ClientListScreen/ClientListScreen.xml',
        'static/src/xml/Screens/OrderManagementScreen/ControlButtons/InvoiceButton.xml',
        'static/src/xml/Screens/OrderManagementScreen/ControlButtons/ReprintReceiptButton.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderManagementScreen.xml',
        'static/src/xml/Screens/OrderManagementScreen/MobileOrderManagementScreen.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderManagementControlPanel.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderList.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderRow.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderDetails.xml',
        'static/src/xml/Screens/OrderManagementScreen/OrderlineDetails.xml',
        'static/src/xml/Screens/OrderManagementScreen/ReprintReceiptScreen.xml',
        'static/src/xml/Screens/TicketScreen/TicketScreen.xml',
        'static/src/xml/Screens/PaymentScreen/PSNumpadInputButton.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreenNumpad.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreenElectronicPayment.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreenPaymentLines.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreenStatus.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentMethodButton.xml',
        'static/src/xml/Screens/PaymentScreen/PaymentScreen.xml',
        'static/src/xml/Screens/ProductScreen/Orderline.xml',
        'static/src/xml/Screens/ProductScreen/OrderSummary.xml',
        'static/src/xml/Screens/ProductScreen/OrderWidget.xml',
        'static/src/xml/Screens/ProductScreen/NumpadWidget.xml',
        'static/src/xml/Screens/ProductScreen/ActionpadWidget.xml',
        'static/src/xml/Screens/ProductScreen/CategoryBreadcrumb.xml',
        'static/src/xml/Screens/ProductScreen/CashBoxOpening.xml',
        'static/src/xml/Screens/ProductScreen/CategoryButton.xml',
        'static/src/xml/Screens/ProductScreen/CategorySimpleButton.xml',
        'static/src/xml/Screens/ProductScreen/HomeCategoryBreadcrumb.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidgetControlPanel.xml',
        'static/src/xml/Screens/ProductScreen/ProductItem.xml',
        'static/src/xml/Screens/ProductScreen/ProductList.xml',
        'static/src/xml/Screens/ProductScreen/ProductsWidget.xml',
        'static/src/xml/Screens/ReceiptScreen/WrappedProductNameLines.xml',
        'static/src/xml/Screens/ReceiptScreen/OrderReceipt.xml',
        'static/src/xml/Screens/ReceiptScreen/ReceiptScreen.xml',
        'static/src/xml/Screens/ScaleScreen/ScaleScreen.xml',
        'static/src/xml/ChromeWidgets/CashierName.xml',
        'static/src/xml/ChromeWidgets/ProxyStatus.xml',
        'static/src/xml/ChromeWidgets/SyncNotification.xml',
        'static/src/xml/ChromeWidgets/OrderManagementButton.xml',
        'static/src/xml/ChromeWidgets/HeaderButton.xml',
        'static/src/xml/ChromeWidgets/SaleDetailsButton.xml',
        'static/src/xml/ChromeWidgets/TicketButton.xml',
        'static/src/xml/SaleDetailsReport.xml',
        'static/src/xml/Misc/Draggable.xml',
        'static/src/xml/Misc/NotificationSound.xml',
        'static/src/xml/Misc/SearchBar.xml',
        'static/src/xml/ChromeWidgets/DebugWidget.xml',
        'static/src/xml/Popups/ErrorPopup.xml',
        'static/src/xml/Popups/ErrorBarcodePopup.xml',
        'static/src/xml/Popups/ConfirmPopup.xml',
        'static/src/xml/Popups/TextInputPopup.xml',
        'static/src/xml/Popups/TextAreaPopup.xml',
        'static/src/xml/Popups/ErrorTracebackPopup.xml',
        'static/src/xml/Popups/SelectionPopup.xml',
        'static/src/xml/Popups/EditListInput.xml',
        'static/src/xml/Popups/EditListPopup.xml',
        'static/src/xml/Popups/NumberPopup.xml',
        'static/src/xml/Popups/OfflineErrorPopup.xml',
        'static/src/xml/Popups/OrderImportPopup.xml',
        'static/src/xml/Popups/ProductConfiguratorPopup.xml',
        'static/src/xml/Screens/ProductScreen/ControlButtons/SetPricelistButton.xml',
        'static/src/xml/Screens/ProductScreen/ControlButtons/SetFiscalPositionButton.xml',
        'static/src/xml/ChromeWidgets/ClientScreenButton.xml',
        'static/src/xml/Misc/MobileOrderWidget.xml',
    ],
    'website': 'https://www.swissconsultings.ch/page/point-of-sale-shop',
    'license': 'LGPL-3',
}
