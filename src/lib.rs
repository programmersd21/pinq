use pyo3::prelude::*;
use pyo3::exceptions::PyRuntimeError;

// ============================================================================
// ERROR HANDLING
// ============================================================================

#[derive(Debug)]
pub enum PinqError {
    NotTTY,
    OperationCanceled,
    InvalidConfiguration(String),
    IOError(String),
    Custom(String),
}

impl std::fmt::Display for PinqError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PinqError::NotTTY => write!(f, "Input is not a TTY"),
            PinqError::IOError(msg) => write!(f, "IO Error: {}", msg),
            PinqError::OperationCanceled => write!(f, "Operation canceled by user"),
            PinqError::InvalidConfiguration(msg) => write!(f, "Invalid configuration: {}", msg),
            PinqError::Custom(msg) => write!(f, "{}", msg),
        }
    }
}

impl From<inquire::InquireError> for PinqError {
    fn from(err: inquire::InquireError) -> Self {
        match err {
            inquire::InquireError::NotTTY => PinqError::NotTTY,
            inquire::InquireError::OperationCanceled => PinqError::OperationCanceled,
            inquire::InquireError::InvalidConfiguration(msg) => PinqError::InvalidConfiguration(msg),
            _ => PinqError::Custom(format!("Unknown error: {:?}", err)),
        }
    }
}

impl From<PinqError> for PyErr {
    fn from(err: PinqError) -> Self {
        PyRuntimeError::new_err(err.to_string())
    }
}

// ============================================================================
// PASSWORD DISPLAY MODE ENUM
// ============================================================================

#[pyclass]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum PasswordDisplayMode {
    #[default]
    Masked,
    Hidden,
}

#[pymethods]
impl PasswordDisplayMode {
    fn __repr__(&self) -> String {
        match self {
            PasswordDisplayMode::Masked => "PasswordDisplayMode.Masked".to_string(),
            PasswordDisplayMode::Hidden => "PasswordDisplayMode.Hidden".to_string(),
        }
    }
}

// ============================================================================
// ACTION ENUMS
// ============================================================================

#[pyclass]
#[derive(Debug, Clone, Copy, PartialEq, Eq, Default)]
pub enum InputAction {
    #[default]
    NoChange,
    Submit,
    Cancel,
    Interrupt,
}

#[pymethods]
impl InputAction {
    fn __repr__(&self) -> String {
        match self {
            InputAction::NoChange => "InputAction.NoChange".to_string(),
            InputAction::Submit => "InputAction.Submit".to_string(),
            InputAction::Cancel => "InputAction.Cancel".to_string(),
            InputAction::Interrupt => "InputAction.Interrupt".to_string(),
        }
    }
}

// ============================================================================
// TEXT PROMPT
// ============================================================================

#[pyclass]
pub struct TextPrompt {
    message: String,
    default: Option<String>,
    help_message: Option<String>,
    page_size: usize,
}

#[pymethods]
impl TextPrompt {
    #[new]
    fn new(message: String) -> Self {
        TextPrompt {
            message,
            default: None,
            help_message: None,
            page_size: 7,
        }
    }

    fn with_default(&mut self, default: String) -> Self {
        self.default = Some(default);
        Self {
            message: self.message.clone(),
            default: self.default.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            default: self.default.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn with_page_size(&mut self, size: usize) -> Self {
        self.page_size = size;
        Self {
            message: self.message.clone(),
            default: self.default.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn prompt(&self) -> PyResult<String> {
        let mut prompt = inquire::Text::new(&self.message);

        if let Some(ref default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<String>> {
        let mut prompt = inquire::Text::new(&self.message);

        if let Some(ref default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// CONFIRM PROMPT
// ============================================================================

#[pyclass]
pub struct ConfirmPrompt {
    message: String,
    default: Option<bool>,
    help_message: Option<String>,
}

#[pymethods]
impl ConfirmPrompt {
    #[new]
    fn new(message: String) -> Self {
        ConfirmPrompt {
            message,
            default: None,
            help_message: None,
        }
    }

    fn with_default(&mut self, default: bool) -> Self {
        self.default = Some(default);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<bool> {
        let mut prompt = inquire::Confirm::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<bool>> {
        let mut prompt = inquire::Confirm::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// PASSWORD PROMPT
// ============================================================================

#[pyclass]
pub struct PasswordPrompt {
    message: String,
    help_message: Option<String>,
}

#[pymethods]
impl PasswordPrompt {
    #[new]
    fn new(message: String) -> Self {
        PasswordPrompt {
            message,
            help_message: None,
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<String> {
        let mut prompt = inquire::Password::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<String>> {
        let mut prompt = inquire::Password::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// SELECT PROMPT
// ============================================================================

#[pyclass]
pub struct SelectPrompt {
    message: String,
    options: Vec<String>,
    default: Option<usize>,
    help_message: Option<String>,
    page_size: usize,
}

#[pymethods]
impl SelectPrompt {
    #[new]
    fn new(message: String, options: Vec<String>) -> PyResult<Self> {
        if options.is_empty() {
            return Err(PyRuntimeError::new_err("Options list cannot be empty"));
        }
        Ok(SelectPrompt {
            message,
            options,
            default: None,
            help_message: None,
            page_size: 7,
        })
    }

    fn with_default(&mut self, index: usize) -> PyResult<Self> {
        if index >= self.options.len() {
            return Err(PyRuntimeError::new_err("Default index out of range"));
        }
        self.default = Some(index);
        Ok(Self {
            message: self.message.clone(),
            options: self.options.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        })
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            options: self.options.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn with_page_size(&mut self, size: usize) -> Self {
        self.page_size = size;
        Self {
            message: self.message.clone(),
            options: self.options.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn prompt(&self) -> PyResult<String> {
        let mut prompt = inquire::Select::new(&self.message, self.options.clone());

        if let Some(idx) = self.default {
            prompt = prompt.with_starting_cursor(idx);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<String>> {
        let mut prompt = inquire::Select::new(&self.message, self.options.clone());

        if let Some(idx) = self.default {
            prompt = prompt.with_starting_cursor(idx);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// MULTISELECT PROMPT
// ============================================================================

#[pyclass]
pub struct MultiSelectPrompt {
    message: String,
    options: Vec<String>,
    defaults: Vec<usize>,
    help_message: Option<String>,
    page_size: usize,
}

#[pymethods]
impl MultiSelectPrompt {
    #[new]
    fn new(message: String, options: Vec<String>) -> PyResult<Self> {
        if options.is_empty() {
            return Err(PyRuntimeError::new_err("Options list cannot be empty"));
        }
        Ok(MultiSelectPrompt {
            message,
            options,
            defaults: vec![],
            help_message: None,
            page_size: 7,
        })
    }

    fn with_defaults(&mut self, indices: Vec<usize>) -> PyResult<Self> {
        for idx in &indices {
            if *idx >= self.options.len() {
                return Err(PyRuntimeError::new_err("Default index out of range"));
            }
        }
        self.defaults = indices;
        Ok(Self {
            message: self.message.clone(),
            options: self.options.clone(),
            defaults: self.defaults.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        })
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            options: self.options.clone(),
            defaults: self.defaults.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn with_page_size(&mut self, size: usize) -> Self {
        self.page_size = size;
        Self {
            message: self.message.clone(),
            options: self.options.clone(),
            defaults: self.defaults.clone(),
            help_message: self.help_message.clone(),
            page_size: self.page_size,
        }
    }

    fn prompt(&self) -> PyResult<Vec<String>> {
        let mut prompt = inquire::MultiSelect::new(&self.message, self.options.clone());

        if !self.defaults.is_empty() {
            prompt = prompt.with_default(&self.defaults);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<Vec<String>>> {
        let mut prompt = inquire::MultiSelect::new(&self.message, self.options.clone());

        if !self.defaults.is_empty() {
            prompt = prompt.with_default(&self.defaults);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt = prompt.with_page_size(self.page_size);

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// CUSTOM TYPE PROMPT (for integers)
// ============================================================================

#[pyclass]
pub struct IntPrompt {
    message: String,
    default: Option<i64>,
    help_message: Option<String>,
}

#[pymethods]
impl IntPrompt {
    #[new]
    fn new(message: String) -> Self {
        IntPrompt {
            message,
            default: None,
            help_message: None,
        }
    }

    fn with_default(&mut self, default: i64) -> Self {
        self.default = Some(default);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<i64> {
        let mut prompt = inquire::CustomType::<i64>::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<i64>> {
        let mut prompt = inquire::CustomType::<i64>::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// FLOAT PROMPT
// ============================================================================

#[pyclass]
pub struct FloatPrompt {
    message: String,
    default: Option<f64>,
    help_message: Option<String>,
}

#[pymethods]
impl FloatPrompt {
    #[new]
    fn new(message: String) -> Self {
        FloatPrompt {
            message,
            default: None,
            help_message: None,
        }
    }

    fn with_default(&mut self, default: f64) -> Self {
        self.default = Some(default);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            default: self.default,
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<f64> {
        let mut prompt = inquire::CustomType::<f64>::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<f64>> {
        let mut prompt = inquire::CustomType::<f64>::new(&self.message);

        if let Some(default) = self.default {
            prompt = prompt.with_default(default);
        }

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// DATE SELECT PROMPT (when date feature is enabled)
// ============================================================================

#[pyclass]
pub struct DateSelectPrompt {
    message: String,
    help_message: Option<String>,
}

#[pymethods]
impl DateSelectPrompt {
    #[new]
    fn new(message: String) -> Self {
        DateSelectPrompt {
            message,
            help_message: None,
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<String> {
        let mut prompt = inquire::DateSelect::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        let date = prompt.prompt().map_err(|e| PinqError::from(e))?;
        Ok(date.to_string())
    }

    fn prompt_skippable(&self) -> PyResult<Option<String>> {
        let mut prompt = inquire::DateSelect::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable()
            .map_err(|e| PinqError::from(e).into())
            .map(|opt| opt.map(|d| d.to_string()))
    }
}

// ============================================================================
// EDITOR PROMPT (when editor feature is enabled)
// ============================================================================

#[pyclass]
pub struct EditorPrompt {
    message: String,
    help_message: Option<String>,
}

#[pymethods]
impl EditorPrompt {
    #[new]
    fn new(message: String) -> Self {
        EditorPrompt {
            message,
            help_message: None,
        }
    }

    fn with_help_message(&mut self, help: String) -> Self {
        self.help_message = Some(help);
        Self {
            message: self.message.clone(),
            help_message: self.help_message.clone(),
        }
    }

    fn prompt(&self) -> PyResult<String> {
        let mut prompt = inquire::Editor::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt().map_err(|e| PinqError::from(e).into())
    }

    fn prompt_skippable(&self) -> PyResult<Option<String>> {
        let mut prompt = inquire::Editor::new(&self.message);

        if let Some(ref help) = self.help_message {
            prompt = prompt.with_help_message(help);
        }

        prompt.prompt_skippable().map_err(|e| PinqError::from(e).into())
    }
}

// ============================================================================
// CONVENIENCE ONE-LINER FUNCTIONS
// ============================================================================

#[pyfunction]
fn prompt_text(message: &str) -> PyResult<String> {
    inquire::Text::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_secret(message: &str) -> PyResult<String> {
    inquire::Password::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_confirmation(message: &str) -> PyResult<bool> {
    inquire::Confirm::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_int(message: &str) -> PyResult<i64> {
    inquire::CustomType::<i64>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_float(message: &str) -> PyResult<f64> {
    inquire::CustomType::<f64>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_u32(message: &str) -> PyResult<u32> {
    inquire::CustomType::<u32>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_u64(message: &str) -> PyResult<u64> {
    inquire::CustomType::<u64>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_f32(message: &str) -> PyResult<f32> {
    inquire::CustomType::<f32>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_f64(message: &str) -> PyResult<f64> {
    inquire::CustomType::<f64>::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e).into())
}

#[pyfunction]
fn prompt_date(message: &str) -> PyResult<String> {
    let date = inquire::DateSelect::new(message)
        .prompt()
        .map_err(|e| PinqError::from(e))?;
    Ok(date.to_string())
}

// ============================================================================
// MODULE INITIALIZATION
// ============================================================================

#[allow(deprecated)]
#[pymodule]
fn pinq(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PasswordDisplayMode>()?;
    m.add_class::<InputAction>()?;
    m.add_class::<TextPrompt>()?;
    m.add_class::<ConfirmPrompt>()?;
    m.add_class::<PasswordPrompt>()?;
    m.add_class::<SelectPrompt>()?;
    m.add_class::<MultiSelectPrompt>()?;
    m.add_class::<IntPrompt>()?;
    m.add_class::<FloatPrompt>()?;
    m.add_class::<DateSelectPrompt>()?;
    m.add_class::<EditorPrompt>()?;

    m.add_function(wrap_pyfunction!(prompt_text, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_secret, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_confirmation, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_int, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_float, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_u32, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_u64, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_f32, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_f64, m)?)?;
    m.add_function(wrap_pyfunction!(prompt_date, m)?)?;

    let version = env!("CARGO_PKG_VERSION");
    m.add("__version__", version)?;

    Ok(())
}
