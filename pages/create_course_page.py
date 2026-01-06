from playwright.sync_api import Page, expect

from pages.base_page import BasePage

class CreateCoursePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.create_course_title = page.get_by_test_id('create-course-toolbar-title-text')
        self.create_course_button = page.get_by_test_id('create-course-toolbar-create-course-button')

        self.preview_image = page.get_by_test_id('create-course-preview-image-upload-widget-preview-image')
        self.preview_empty_view_icon = page.get_by_test_id('create-course-preview-empty-view-icon')
        self.preview_empty_view_title = page.get_by_test_id('create-course-preview-empty-view-title-text')
        self.preview_empty_view_description = page.get_by_test_id('create-course-preview-empty-view-description-text')

        self.preview_image_upload_icon = page.get_by_test_id('create-course-preview-image-upload-widget-info-icon')
        self.preview_image_upload_title = page.get_by_test_id('create-course-preview-image-upload-widget-info-title-text')
        self.preview_image_upload_description = page.get_by_test_id('create-course-preview-image-upload-widget-info-description-text')
        self.preview_image_upload_button = page.get_by_test_id('create-course-preview-image-upload-widget-upload-button')
        self.preview_image_remove_button = page.get_by_test_id('create-course-preview-image-upload-widget-remove-button')
        self.preview_image_upload_input = page.get_by_test_id('create-course-preview-image-upload-widget-input')

        self.create_course_title_input = page.get_by_test_id('create-course-form-title-input').locator('input')
        self.create_course_estimate_input = page.get_by_test_id('create-course-form-estimated-time-input').locator('input')
        self.create_course_description_textarea = page.get_by_test_id('create-course-form-description-input').locator('textarea').first
        self.create_course_max_score_input = page.get_by_test_id('create-course-form-max-score-input').locator('input')
        self.create_course_min_score_input = page.get_by_test_id('create-course-form-min-score-input').locator('input')

        self.exercises_title = page.get_by_test_id('create-course-exercises-box-toolbar-title-text')
        self.creat_exercises_button = page.get_by_test_id('create-course-exercises-box-toolbar-create-exercise-button')

        self.exercises_empty_view_icon = page.get_by_test_id('create-course-exercises-empty-view-icon')
        self.exercises_empty_view_title = page.get_by_test_id('create-course-exercises-empty-view-title-text')
        self.exercises_empty_view_description = page.get_by_test_id('create-course-exercises-empty-view-description-text')

    def check_visible_create_course_title(self):
        expect(self.create_course_title).to_be_visible()
        expect(self.create_course_title).to_have_text('Create Course')

    def click_create_course_title(self):
        self.create_course_button.click()

    def check_visible_create_course_button(self):
        expect(self.check_visible_create_course_button).to_be_visible()

    def check_disable_create_course_button(self):
        expect(self.create_course_button).to_be_disabled()

    def check_visible_image_preview_empty_view(self):
        expect(self.preview_empty_view_icon).to_be_visible()

        expect(self.preview_empty_view_title).to_be_visible()
        expect(self.preview_empty_view_title).to_have_text('No image selected')

        expect(self.preview_empty_view_description).to_be_visible()
        expect(self.preview_empty_view_description).to_have_text('Preview of selected image will be displayed here')

    def check_visible_image_upload_view(self, is_image_uploaded: bool= False):
        expect(self.preview_image_upload_icon).to_be_visible()

        expect(self.preview_image_upload_title).to_be_visible()
        expect(self.preview_image_upload_title).to_have_text('Tap on "Upload image" button to select file')

        expect(self.preview_image_upload_description).to_be_visible()
        expect(self.preview_image_upload_description).to_have_text('Recommended file size 540X300')

        expect(self.preview_image_upload_button).to_be_visible()

        if is_image_uploaded:
            expect(self.preview_image_remove_button).to_be_visible()  # Ставим проверку, что может быть 2 состояния

    def click_remove_image_button(self):
        self.preview_image_remove_button.click()

    def check_visible_preview_image(self):
        expect(self.preview_image).to_be_visible()

    def upload_preview_image(self, file: str): # Метод с загрузкой файла
        self.preview_image_upload_input.set_input_files()

    def check_visible_create_course_form(
            self,
            title: str,
            estimated_time: str,
            description: str,
            max_score: int,
            min_score: int,
    ):
        expect(self.create_course_title_input).to_be_visible()
        expect(self.create_course_title_input).to_have_value(title)

        expect(self.create_course_estimate_input).to_be_visible()
        expect(self.create_course_estimate_input).to_have_value(estimated_time)

        expect(self.create_course_description_textarea).to_be_visible()
        expect(self.create_course_description_textarea).to_have_value(description)

        expect(self.create_course_max_score_input).to_be_visible()
        expect(self.create_course_max_score_input).to_have_value(max_score)

        expect(self.create_course_min_score_input).to_be_visible()
        expect(self.create_course_min_score_input).to_have_value(min_score)

    def check_visible_exercises_title(self):
        expect(self.exercises_title).to_be_visible()
        expect(self.exercises_title).to_have_text('Exercises')

    def check_visible_create_exercises_button(self):
        expect(self.create_course_button).to_be_visible()

    def click_create_exercises_button(self):
        self.create_course_button.click()

    def check_visible_exercises_empty_view(self):
        expect(self.exercises_empty_view_icon).to_be_visible()

        expect(self.exercises_empty_view_title).to_be_visible()
        expect(self.exercises_empty_view_title).to_have_text('There is no exercises')

        expect(self.exercises_empty_view_description).to_be_visible()
        expect(self.exercises_empty_view_description).to_have_text('Click on "Create exercise" button to create new exercise')

    def click_delete_exercises_button(self, index: int): #Индекс для динамического локатора
        delete_exercises_button = self.page.get_by_test_id(f'create-course-exercise-{index}-box-toolbar-delete-exercise-button')
        delete_exercises_button.click()

    def check_visible_create_exercises_form(self, index: int, title: str, description: str):
        exercises_subtitle = self.page.get_by_id(f'create-course-exercise-{index}-box-toolbar-subtitle-text')

        exercises_title_input = self.page.get_by_id(f'create-course-exercise-form-title-{index}-input')

        exercises_description_input = self.page.get_by_id(f'create-course-exercise-form-description-{index}-input')

        expect(exercises_subtitle).to_be_visible()
        expect(exercises_subtitle).to_have_text(f'#{index + 1}Exercise')

        expect(exercises_title_input).to_be_visible()
        expect(exercises_title_input).to_have_value(title)

        expect(exercises_description_input).to_be_visible()
        expect(exercises_description_input).to_have_value(description)
