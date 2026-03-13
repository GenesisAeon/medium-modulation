"""CLI mm – medium-modulation command-line interface."""

import numpy as np
import typer
from rich.console import Console
from rich.table import Table

from .core import coupling_factor, modulated_entropy, resonance_spectrum

app = typer.Typer(
    help="medium-modulation CLI – fractal entropy coupling between S∝A and S∝V"
)
console = Console()


@app.command()
def modulate(
    depth: float = typer.Option(0.5, help="Modulation depth in [0, 1]"),
    freq: float = typer.Option(1.0, help="Modulation frequency (rad/s)"),
    steps: int = typer.Option(100, help="Number of time steps over [0, 10]"),
    s_a: float = typer.Option(1.0, help="Action-governed entropy S_A"),
    s_v: float = typer.Option(1.618, help="Volume-governed entropy S_V"),
) -> None:
    """Apply fractal modulation to the S_A/S_V entropy duality."""
    t_range = np.linspace(0, 10, steps)
    s_mod = [modulated_entropy(s_a, s_v, depth, freq, ti) for ti in t_range]
    arr = np.array(s_mod)

    table = Table(title="Modulation Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Mean S_mod", f"{arr.mean():.6f}")
    table.add_row("Min S_mod", f"{arr.min():.6f}")
    table.add_row("Max S_mod", f"{arr.max():.6f}")
    table.add_row("Std S_mod", f"{arr.std():.6f}")
    table.add_row("depth", str(depth))
    table.add_row("freq", str(freq))
    table.add_row("steps", str(steps))

    console.print(table)


@app.command()
def spectrum(
    f_min: float = typer.Option(0.1, help="Minimum frequency"),
    f_max: float = typer.Option(10.0, help="Maximum frequency"),
    n: int = typer.Option(50, help="Number of frequency points"),
    depth: float = typer.Option(0.5, help="Modulation depth in [0, 1]"),
) -> None:
    """Show the resonance spectrum over a frequency range."""
    freqs = np.linspace(f_min, f_max, n)
    spec = resonance_spectrum(freqs, depth)

    table = Table(title="Resonance Spectrum")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Peak amplitude", f"{spec.max():.6f}")
    table.add_row("Min amplitude", f"{spec.min():.6f}")
    table.add_row("Mean amplitude", f"{spec.mean():.6f}")
    table.add_row("Peak frequency", f"{freqs[spec.argmax()]:.4f} rad/s")

    console.print(table)


@app.command()
def couple(
    a: float = typer.Option(1.0, help="Action amplitude A"),
    v: float = typer.Option(1.618, help="Volume amplitude V"),
    depth: float = typer.Option(0.5, help="Modulation depth in [0, 1]"),
) -> None:
    """Compute dynamic coupling strength between action and volume."""
    kappa = coupling_factor(a, v, modulation_depth=depth)
    console.print(
        f"[bold cyan]Coupling factor k(A={a}, V={v}, depth={depth}):[/] "
        f"[green]{kappa:.6f}[/]"
    )


if __name__ == "__main__":
    app()
