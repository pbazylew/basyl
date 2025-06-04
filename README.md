basyl
=====

This repository contains two example graphical Python programs using `tkinter`.

* `simple_gui.py` – displays a basic window with a greeting and a close button.
* `inventory_gui.py` – a simple warehouse inventory application.

## Running the examples

All scripts require Python 3 with the standard `tkinter` and `sqlite3` modules.

```bash
python3 simple_gui.py       # run the minimal demo
python3 inventory_gui.py    # run the inventory manager
```

The inventory application (`inventory_gui.py`) allows you to:

* add new products (Produktname, Anzahl, Preis)
* edit or delete the selected product
* store data persistently in a local SQLite database (`inventory.db`)

All interface labels are in German. The code is organised so new modules or
features can be added easily.

