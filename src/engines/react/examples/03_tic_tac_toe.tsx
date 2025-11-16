// Tic-Tac-Toe Game

const { createElement: h, useState, useEffect, useCallback, useMemo, useRef } = React;
const { createRoot } = ReactDOM;

function App() {
  const [board, setBoard] = useState(Array(9).fill(null));
  const [isXNext, setIsXNext] = useState(true);
  const [winner, setWinner] = useState(null);
  const [winningLine, setWinningLine] = useState([]);

  const winningCombinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], // rows
    [0, 3, 6], [1, 4, 7], [2, 5, 8], // columns
    [0, 4, 8], [2, 4, 6]             // diagonals
  ];

  const calculateWinner = (squares) => {
    for (let combination of winningCombinations) {
      const [a, b, c] = combination;
      if (squares[a] && squares[a] === squares[b] && squares[a] === squares[c]) {
        return { winner: squares[a], line: combination };
      }
    }
    return null;
  };

  const handleClick = (index) => {
    if (board[index] || winner) return;

    const newBoard = [...board];
    newBoard[index] = isXNext ? 'X' : 'O';
    setBoard(newBoard);

    const result = calculateWinner(newBoard);
    if (result) {
      setWinner(result.winner);
      setWinningLine(result.line);
    } else {
      setIsXNext(!isXNext);
    }
  };

  const resetGame = () => {
    setBoard(Array(9).fill(null));
    setIsXNext(true);
    setWinner(null);
    setWinningLine([]);
  };

  const isBoardFull = board.every(cell => cell !== null);
  const isDraw = isBoardFull && !winner;

  const getSquareStyle = (index) => {
    const baseStyle = {
      width: '100px',
      height: '100px',
      fontSize: '3rem',
      fontWeight: 'bold',
      backgroundColor: 'white',
      border: '3px solid #1a73e8',
      cursor: board[index] || winner ? 'not-allowed' : 'pointer',
      transition: 'all 0.2s',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: board[index] === 'X' ? '#ef4444' : '#10b981',
    };

    if (winningLine.includes(index)) {
      baseStyle.backgroundColor = '#fef3c7';
      baseStyle.borderColor = '#f59e0b';
    }

    return baseStyle;
  };

  return h('div', {
    style: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '500px',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      padding: '2rem',
    }
  },
    h('h1', {
      style: {
        fontSize: '3rem',
        marginBottom: '1rem',
        color: '#1a73e8',
      }
    }, 'Tic-Tac-Toe'),

    // Status display
    h('div', {
      style: {
        fontSize: '1.5rem',
        fontWeight: '600',
        marginBottom: '2rem',
        padding: '1rem 2rem',
        backgroundColor: winner ? '#fef3c7' : isDraw ? '#f3f4f6' : '#dbeafe',
        borderRadius: '12px',
        color: winner ? '#92400e' : isDraw ? '#374151' : '#1e40af',
      }
    },
      winner
        ? `🎉 Winner: ${winner}!`
        : isDraw
        ? `🤝 It's a Draw!`
        : `Next player: ${isXNext ? 'X' : 'O'}`
    ),

    // Game board
    h('div', {
      style: {
        display: 'grid',
        gridTemplateColumns: 'repeat(3, 100px)',
        gridTemplateRows: 'repeat(3, 100px)',
        gap: '8px',
        marginBottom: '2rem',
      }
    },
      ...board.map((cell, index) =>
        h('button', {
          key: index,
          onClick: () => handleClick(index),
          style: getSquareStyle(index),
          onMouseEnter: (e) => {
            if (!cell && !winner) {
              e.target.style.backgroundColor = '#f0f9ff';
            }
          },
          onMouseLeave: (e) => {
            if (!winningLine.includes(index)) {
              e.target.style.backgroundColor = 'white';
            }
          },
        }, cell || '')
      )
    ),

    // Reset button
    h('button', {
      onClick: resetGame,
      style: {
        padding: '1rem 2rem',
        fontSize: '1.2rem',
        backgroundColor: '#6b7280',
        color: 'white',
        border: 'none',
        borderRadius: '8px',
        cursor: 'pointer',
        fontWeight: '600',
        transition: 'all 0.2s',
      },
      onMouseEnter: (e) => {
        e.target.style.backgroundColor = '#4b5563';
        e.target.style.transform = 'scale(1.05)';
      },
      onMouseLeave: (e) => {
        e.target.style.backgroundColor = '#6b7280';
        e.target.style.transform = 'scale(1)';
      },
    }, '🔄 New Game'),

    // Game info
    h('div', {
      style: {
        marginTop: '2rem',
        padding: '1rem',
        backgroundColor: '#f9fafb',
        borderRadius: '8px',
        textAlign: 'center',
        color: '#6b7280',
        fontSize: '0.875rem',
      }
    },
      h('p', { style: { margin: '0' } }, 'Click on a square to make your move.'),
      h('p', { style: { margin: '0.5rem 0 0 0' } },
        h('span', { style: { color: '#ef4444', fontWeight: 'bold' } }, 'X'),
        ' vs ',
        h('span', { style: { color: '#10b981', fontWeight: 'bold' } }, 'O')
      )
    )
  );
}

const root = createRoot(document.getElementById('root'));
root.render(h(App));

export {}; // Make this file a module to avoid global scope conflicts
