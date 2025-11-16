// Todo List App with CRUD Operations

function App() {
  const [todos, setTodos] = useState([
    { id: 1, text: 'Learn React', completed: false },
    { id: 2, text: 'Build a todo app', completed: false },
    { id: 3, text: 'Master TypeScript', completed: false },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editingText, setEditingText] = useState('');

  // Create
  const addTodo = () => {
    if (inputValue.trim() === '') return;

    const newTodo = {
      id: Date.now(),
      text: inputValue,
      completed: false,
    };
    setTodos([...todos, newTodo]);
    setInputValue('');
  };

  // Update - Toggle completion
  const toggleTodo = (id) => {
    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, completed: !todo.completed } : todo
    ));
  };

  // Update - Edit text
  const startEditing = (todo) => {
    setEditingId(todo.id);
    setEditingText(todo.text);
  };

  const saveEdit = (id) => {
    if (editingText.trim() === '') return;

    setTodos(todos.map(todo =>
      todo.id === id ? { ...todo, text: editingText } : todo
    ));
    setEditingId(null);
    setEditingText('');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditingText('');
  };

  // Delete
  const deleteTodo = (id) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addTodo();
    }
  };

  const handleEditKeyPress = (e, id) => {
    if (e.key === 'Enter') {
      saveEdit(id);
    } else if (e.key === 'Escape') {
      cancelEdit();
    }
  };

  return h('div', {
    style: {
      maxWidth: '600px',
      margin: '0 auto',
      padding: '2rem',
      fontFamily: 'system-ui, -apple-system, sans-serif',
    }
  },
    h('h1', {
      style: {
        fontSize: '2.5rem',
        marginBottom: '2rem',
        color: '#1a73e8',
        textAlign: 'center',
      }
    }, 'Todo List'),

    // Input section
    h('div', {
      style: {
        display: 'flex',
        gap: '0.5rem',
        marginBottom: '2rem',
      }
    },
      h('input', {
        type: 'text',
        value: inputValue,
        onChange: (e) => setInputValue(e.target.value),
        onKeyPress: handleKeyPress,
        placeholder: 'Add a new todo...',
        style: {
          flex: 1,
          padding: '0.75rem',
          fontSize: '1rem',
          border: '2px solid #e5e7eb',
          borderRadius: '8px',
          outline: 'none',
        },
        onFocus: (e) => {
          e.target.style.borderColor = '#1a73e8';
        },
        onBlur: (e) => {
          e.target.style.borderColor = '#e5e7eb';
        },
      }),
      h('button', {
        onClick: addTodo,
        style: {
          padding: '0.75rem 1.5rem',
          fontSize: '1rem',
          backgroundColor: '#1a73e8',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          fontWeight: '500',
        },
        onMouseEnter: (e) => {
          e.target.style.backgroundColor = '#1557b0';
        },
        onMouseLeave: (e) => {
          e.target.style.backgroundColor = '#1a73e8';
        },
      }, 'Add')
    ),

    // Todo list
    h('div', {
      style: {
        display: 'flex',
        flexDirection: 'column',
        gap: '0.5rem',
      }
    },
      ...todos.map(todo =>
        h('div', {
          key: todo.id,
          style: {
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
            padding: '1rem',
            backgroundColor: todo.completed ? '#f3f4f6' : 'white',
            border: '1px solid #e5e7eb',
            borderRadius: '8px',
            transition: 'all 0.2s',
          }
        },
          // Checkbox
          h('input', {
            type: 'checkbox',
            checked: todo.completed,
            onChange: () => toggleTodo(todo.id),
            style: {
              width: '1.25rem',
              height: '1.25rem',
              cursor: 'pointer',
            }
          }),

          // Text or Edit Input
          editingId === todo.id
            ? h('input', {
                type: 'text',
                value: editingText,
                onChange: (e) => setEditingText(e.target.value),
                onKeyPress: (e) => handleEditKeyPress(e, todo.id),
                autoFocus: true,
                style: {
                  flex: 1,
                  padding: '0.5rem',
                  fontSize: '1rem',
                  border: '2px solid #1a73e8',
                  borderRadius: '4px',
                  outline: 'none',
                }
              })
            : h('span', {
                style: {
                  flex: 1,
                  fontSize: '1rem',
                  textDecoration: todo.completed ? 'line-through' : 'none',
                  color: todo.completed ? '#9ca3af' : '#1f2937',
                }
              }, todo.text),

          // Action buttons
          editingId === todo.id
            ? h('div', {
                style: {
                  display: 'flex',
                  gap: '0.5rem',
                }
              },
                h('button', {
                  onClick: () => saveEdit(todo.id),
                  style: {
                    padding: '0.5rem 1rem',
                    fontSize: '0.875rem',
                    backgroundColor: '#10b981',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }
                }, 'Save'),
                h('button', {
                  onClick: cancelEdit,
                  style: {
                    padding: '0.5rem 1rem',
                    fontSize: '0.875rem',
                    backgroundColor: '#6b7280',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  }
                }, 'Cancel')
              )
            : h('div', {
                style: {
                  display: 'flex',
                  gap: '0.5rem',
                }
              },
                h('button', {
                  onClick: () => startEditing(todo),
                  style: {
                    padding: '0.5rem 1rem',
                    fontSize: '0.875rem',
                    backgroundColor: '#f59e0b',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  },
                  onMouseEnter: (e) => {
                    e.target.style.backgroundColor = '#d97706';
                  },
                  onMouseLeave: (e) => {
                    e.target.style.backgroundColor = '#f59e0b';
                  },
                }, 'Edit'),
                h('button', {
                  onClick: () => deleteTodo(todo.id),
                  style: {
                    padding: '0.5rem 1rem',
                    fontSize: '0.875rem',
                    backgroundColor: '#ef4444',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                  },
                  onMouseEnter: (e) => {
                    e.target.style.backgroundColor = '#dc2626';
                  },
                  onMouseLeave: (e) => {
                    e.target.style.backgroundColor = '#ef4444';
                  },
                }, 'Delete')
              )
        )
      )
    ),

    // Stats
    h('div', {
      style: {
        marginTop: '2rem',
        padding: '1rem',
        backgroundColor: '#f9fafb',
        borderRadius: '8px',
        textAlign: 'center',
        color: '#6b7280',
      }
    },
      h('span', { style: { fontWeight: '500' } },
        `${todos.filter(t => t.completed).length} of ${todos.length} completed`
      )
    )
  );
}
