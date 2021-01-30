<template>
  <link href="https://fonts.googleapis.com/css2?family=Inconsolata:wght@300&display=swap" rel="stylesheet">
  <div class="main">
    <h3 id="state"></h3>
    <div id="sudoku"></div>
    <div class="button-div">
      <button id="solve-button" @click.prevent="solve">Solve</button>
      <button id="clear-button" @click.prevent="clearBoard">Clear</button>
      <button id="copy-button" @click.prevent="copy">Copy textfile</button>
      <button id="toggle-import-button" @click.prevent="toggleImport">Import textfile</button>
    </div>
    <div class="import-div hidden" ref="importDiv">
      <textarea id="import-text" cols="15" rows="9"></textarea>
      <button id="import-button" @click.prevent="importFile">Import</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Index',
  mounted () {
    const sudokuDiv = document.querySelector('#sudoku')
    for (let rowIndex = 0; rowIndex < 9; rowIndex++) {
      const row = document.createElement('div')
      row.className = 'sudoku-row'
      for (let columnIndex = 0; columnIndex < 9; columnIndex++) {
        const input = document.createElement('input')
        input.className = 'sudoku-input'
        input.setAttribute('maxlength', 1)
        input.setAttribute('row', rowIndex)
        input.setAttribute('column', columnIndex)
        row.appendChild(input)
      }
      sudokuDiv.appendChild(row)
    }
  },
  methods: {
    stringify () {
      let sudokuString = ''
      const rows = document.querySelectorAll('.sudoku-row')
      rows.forEach(row => {
        const inputs = row.querySelectorAll('input')
        inputs.forEach(input => {
          sudokuString += input.value !== '' ? input.value : ' '
          sudokuString += ','
        })
        sudokuString = sudokuString.slice(0, -1)
        sudokuString += '\n'
      })
      sudokuString = sudokuString.slice(0, -1)
      return sudokuString
    },

    copy (e) {
      e.preventDefault()
      const sudokuString = this.stringify()
      const copyText = document.createElement('textarea')
      copyText.value = sudokuString
      copyText.setAttribute('readonly', '')
      copyText.style.position = 'absolute'
      copyText.style.left = '-9999px'
      document.body.appendChild(copyText)
      copyText.select()
      document.execCommand('copy')
      document.body.removeChild(copyText)
      alert('Copied text to clipboard')
    },

    setSudoku (rows) {
      const inputRows = document.querySelectorAll('.sudoku-row')
      for (let i = 0; i < 9; i++) {
        const inputs = inputRows[i].querySelectorAll('input')
        for (let j = 0; j < 9; j++) {
          if (rows[i][j].toString() === parseInt(rows[i][j]).toString()) {
            inputs[j].value = rows[i][j]
          } else {
            inputs[j].value = ''
          }
        }
      }
    },

    toggleImport (e) {
      this.$refs.importDiv.classList.toggle('hidden')
    },

    importFile (e) {
      e.preventDefault()
      const text = document.querySelector('#import-text').value
      const rows = text.split('\n')
      if (rows.length !== 9) {
        alert('Wrong format, please correct it and try again!')
        return
      }
      for (let i = 0; i < 9; i++) {
        rows[i] = rows[i].split(',')
        if (rows[i].length !== 9) {
          alert('Wrong format, please correct it and try again!')
          return
        }
      }
      this.setSudoku(rows)
    },

    clearBoard (e) {
      e.preventDefault()
      const rows = Array(9)
      for (let i = 0; i < 9; i++) {
        rows[i] = Array(9)
      }
      this.setSudoku(rows)
    },

    setState (msg) {
      document.querySelector('#state').textContent = msg
    },

    clearState () {
      document.querySelector('#state').textContent = ''
    },

    async solve (e) {
      e.preventDefault()
      this.clearState()
      let sudokuString = this.stringify()
      sudokuString = sudokuString.replaceAll('\n', 'x')
      const response = await fetch(`http://127.0.0.1:5000/${sudokuString}`)
      const jsonResponse = await response.json()
      if (jsonResponse.state === 'Correct!') {
        this.setState('Solved in ' + jsonResponse.time.toFixed(5) + ' seconds')
      } else {
        this.setState(jsonResponse.state)
      }
      this.setSudoku(jsonResponse.sudoku)
    }
  }
}
</script>

<style lang="scss">

.main {
  min-height: 100vh;
  max-width: 1000px;
  margin: auto;
  display: flex;
  align-items: center;
  flex-direction: column;
  textarea {
    font-family: 'Inconsolata', monospace;
  }
  h3 {
    height: fit-content;
  }
  #sudoku {
    width: fit-content;
    border-style: solid;
    border-width: 2px;

    .sudoku-input {
      width: 3rem;
      height: 3rem;
      border-left: none;
      border-bottom: none;
      border-top: none;
      text-align: center;
      font-size: 2rem;
    }

    .sudoku-input:nth-of-type(9) {
      border-right: none;
    }

    .sudoku-row:nth-of-type(3), .sudoku-row:nth-of-type(6) {
      border-bottom-style: solid;
      border-bottom-width: 2px;
    }

    .sudoku-input:nth-of-type(3), .sudoku-input:nth-of-type(6) {
      border-right-style: solid;
      border-right-width: 2px;
    }

    .sudoku-row:nth-of-type(3n + 1), .sudoku-row:nth-of-type(3n + 2) {
      border-bottom-style: solid;
      border-bottom-width: 1px;
    }

    .sudoku-input:nth-of-type(3n + 1), .sudoku-input:nth-of-type(3n + 2) {
      border-right-style: solid;
      border-right-width: 1px;
    }
  }
  .button-div {
    width: 30rem;
    display: flex;
    justify-content: space-evenly;
    button {
      border: none;
      font-size: 1rem;
      padding: 0.75rem 1.5rem;
      transition: ease 1s;
      &:hover {
        transition: ease 1s;
      }
    }
  }
  .import-div {
    display: flex;
    flex-direction: column;
    align-items: center;
    &.hidden {
      display: none;
    }
    button {
      border: none;
      font-size: 1rem;
      padding: 0.75rem 1.5rem;
      transition: ease 1s;
      &:hover {
        transition: ease 1s;
      }
    }
  }
}

body{
  #sudoku {
    border-color: rgb(50, 50, 50);
    .sudoku-row {
      border-color: rgb(50, 50, 50);
    }
    .sudoku-input {
      border-color: rgb(50, 50, 50);
      background: rgb(250, 250, 250);
    }
  }
  .button-div {
    button {
      background-color:rgba(220,220,220,0);
      &:hover {
        background-color:rgba(220,220,220,1);
      }
    }
  }
  .import-div {
    button {
      background-color:rgba(220,220,220,0);
      &:hover {
        background-color:rgba(220,220,220,1);
      }
    }
  }
}

body.dark-theme{
  #sudoku {
    border-color: rgb(150, 150, 150);
    .sudoku-row {
      border-color: rgb(150, 150, 150);
    }
    .sudoku-input {
      border-color: rgb(150, 150, 150);
      background: rgb(50, 50, 50);
    }
  }
  .button-div {
    button {
      background-color:rgba(65,65,65,0);
      &:hover {
        background-color:rgba(65,65,65,1);
      }
    }
  }
  .import-div {
    textarea {
      background: rgb(50, 50, 50);
      border-color: rgb(150,150,150);
    }
    button {
      background-color:rgba(65,65,65,0);
      &:hover {
        background-color:rgba(65,65,65,1);
      }
    }
  }
}

</style>
