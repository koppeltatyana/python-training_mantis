from selenium.webdriver.support.select import Select


class ProjectHelper:

    def __init__(self, app):
        self.app = app

    def create(self, project):
        wd = self.app.wd
        self.return_to_manage_projects_page()
        wd.find_element_by_xpath("//input[@value='Create New Project']").click()
        self.enter_values(project)
        wd.find_element_by_xpath("//input[@value='Add Project']").click()
        self.return_to_manage_projects_page()

    def return_to_manage_projects_page(self):
        self.open_manage_page()
        self.open_manage_projects_page()

    def open_manage_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_overview_page.php"):  # and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("Manage").click()

    def open_manage_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):  # and len(wd.find_elements_by_name("new")) > 0):
            wd.find_element_by_link_text("Manage Projects").click()

    def enter_values(self, project):
        wd = self.app.wd
        self.change_field_value("name", project.name)
        self.change_list_field_value("status", project.status)
        self.change_list_field_value("view_state", project.view_status)
        self.change_field_value("description", project.description)

    def change_field_value(self, field_name, new_value):
        wd = self.app.wd
        # если пришло значение != значению по умолчанию, то меняем значение на новое
        if new_value is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(new_value)

    def change_list_field_value(self, field_name, new_value):
        wd = self.app.wd
        # если пришло значение != значению по умолчанию, то меняем значение на новое
        if new_value is not None:
            wd.find_element_by_name(field_name).click()
            Select(wd.find_element_by_name(field_name)).select_by_visible_text(new_value)
