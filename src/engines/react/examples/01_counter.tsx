// Counter App: Increment, Decrement, and Reset

const { createElement: h, useState, useEffect, useCallback, useMemo, useRef } = React;
const { createRoot } = ReactDOM;

function App() {
  const [count, setCount] = useState(0);

  const increment = () => setCount(count + 1);
  const decrement = () => setCount(count - 1);
  const reset = () => setCount(0);

  return h('div', {
    style: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '400px',
      fontFamily: 'system-ui, -apple-system, sans-serif',
    }
  },
    h('h1', {
      style: {
        fontSize: '3rem',
        margin: '0 0 2rem 0',
        color: '#1a73e8',
      }
    }, 'Counter App'),

    h('div', {
      style: {
        fontSize: '4rem',
        fontWeight: 'bold',
        margin: '0 0 2rem 0',
        color: count === 0 ? '#666' : count > 0 ? '#10b981' : '#ef4444',
        transition: 'color 0.3s ease',
      }
    }, count),

    h('div', {
      style: {
        display: 'flex',
        gap: '1rem',
      }
    },
      h('button', {
        onClick: decrement,
        style: {
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          backgroundColor: '#ef4444',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'transform 0.1s, background-color 0.2s',
        },
        onMouseEnter: (e) => {
          e.target.style.backgroundColor = '#dc2626';
        },
        onMouseLeave: (e) => {
          e.target.style.backgroundColor = '#ef4444';
        },
        onMouseDown: (e) => {
          e.target.style.transform = 'scale(0.95)';
        },
        onMouseUp: (e) => {
          e.target.style.transform = 'scale(1)';
        },
      }, '− Decrement'),

      h('button', {
        onClick: reset,
        style: {
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          backgroundColor: '#6b7280',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'transform 0.1s, background-color 0.2s',
        },
        onMouseEnter: (e) => {
          e.target.style.backgroundColor = '#4b5563';
        },
        onMouseLeave: (e) => {
          e.target.style.backgroundColor = '#6b7280';
        },
        onMouseDown: (e) => {
          e.target.style.transform = 'scale(0.95)';
        },
        onMouseUp: (e) => {
          e.target.style.transform = 'scale(1)';
        },
      }, '↻ Reset'),

      h('button', {
        onClick: increment,
        style: {
          padding: '1rem 2rem',
          fontSize: '1.2rem',
          backgroundColor: '#10b981',
          color: 'white',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          transition: 'transform 0.1s, background-color 0.2s',
        },
        onMouseEnter: (e) => {
          e.target.style.backgroundColor = '#059669';
        },
        onMouseLeave: (e) => {
          e.target.style.backgroundColor = '#10b981';
        },
        onMouseDown: (e) => {
          e.target.style.transform = 'scale(0.95)';
        },
        onMouseUp: (e) => {
          e.target.style.transform = 'scale(1)';
        },
      }, '+ Increment')
    )
  );
}

const root = createRoot(document.getElementById('root'));
root.render(h(App));

export {}; // Make this file a module to avoid global scope conflicts
