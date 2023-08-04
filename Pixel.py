import numpy as np
from decimal import Decimal

ELECTRON_CHARGE = 1.60217663e-19 # charge of an electron
CLOCK_FREQ = 20  # clock period in nanoseconds

class Pixel:
    """
    Represents a pixel in a simulation model.

    Attributes:
        id (tuple): The pixel's unique identifier (x, y).
        prev_time (float): Timestamp of the last reset.
        charge (float): Current charge held on the capacitors.
        active (bool): Whether the pixel is active.
        w_value (float): W value in EV.
        e_val (float): Drift velocity in cm/s.
        diffusion_l (float): Longitudinal diffusion in cm^2/s.
        diffusion_t (float): Transverse diffusion in cm^2/s.
        life_time (float): Electron life time in seconds.
        readout_dim (float): Readout place size in cm.
        pix_size (float): Pixel size in cm.
        reset (int): Number of electrons for reset.
        sample_time (int): Sample time in ns.
        buffer_time (int): Buffer window in ns.
        dead_time (int): Dead time in ns.
        charge_loss (bool): Whether charge loss occurs.
        recombination (bool): Whether recombination occurs.
    """
    def __init__(self, id, prev_time=0.0, charge=0.0, active=True,
                 w_value=23.6, e_val=164800.0, diffusion_l=6.8223,
                 diffusion_t=13.1586, life_time=0.1, readout_dim=100,
                 pix_size=0.4, reset=6250, sample_time=10, buffer_time=1,
                 dead_time=0, charge_loss=False, recombination=True) -> None:
        """
        Initialize a Pixel object.

        Parameters:
            id (tuple): The pixel's unique identifier (x, y).
            prev_time (float): Timestamp of the last reset.
            charge (float): Current charge held on the capacitors.
            active (bool): Whether the pixel is active.
            w_value (float): W value in EV.
            e_val (float): Drift velocity in cm/s.
            diffusion_l (float): Longitudinal diffusion in cm^2/s.
            diffusion_t (float): Transverse diffusion in cm^2/s.
            life_time (float): Electron life time in seconds.
            readout_dim (float): Readout place size in cm.
            pix_size (float): Pixel size in cm.
            reset (int): Number of electrons for reset.
            sample_time (int): Sample time in ns.
            buffer_time (int): Buffer window in ns.
            dead_time (int): Dead time in ns.
            charge_loss (bool): Whether charge loss occurs.
            recombination (bool): Whether recombination occurs.
        """
        self.id = id
        self.charge = charge
        self.prev_time = prev_time
        self.active = active
        self.w_value = w_value
        self.e_val = e_val
        self.diffusion_l = diffusion_l
        self.diffusion_t = diffusion_t
        self.life_time = life_time
        self.readout_dim = readout_dim
        self.pix_size = pix_size
        self.reset = reset
        self.sample_time = sample_time
        self.buffer_time = buffer_time
        self.dead_time = dead_time

    def __str__(self) -> str:
        """
        Get a string representation of the Pixel's parameters and status.

        Returns:
            str: A formatted string containing parameter values and status.
        """
        result = "*******************************************************\n"
        result += "Liquid Argon Parameters\n"
        result += "*******************************************************\n"
        result += "W value                    = {} [eV]\n".format(self.w_value)
        result += "Drift velocity             = {} [cm/s]\n".format(self.e_val)
        result += "Longitudinal diffusion     = {} [cm^2/s]\n".format(self.diffusion_l)
        result += "Transverse diffusion       = {} [cm^2/s]\n".format(self.diffusion_t)
        result += "Electron life time         = {} [s]\n".format(self.life_time)
        result += "Readout dimensions         = {} [cm]\n".format(self.readout_dim)
        result += "Pixel size                 = {} [cm]\n".format(self.pix_size)
        result += "Reset threshold            = {} [electrons]\n".format(self.reset)
        result += "Sample time                = {} [ns]\n".format(self.sample_time)
        result += "Buffer window              = {} [ns]\n".format(self.buffer_time)
        result += "Dead time                  = {} [ns]\n".format(self.dead_time)
        result += "*******************************************************\n"
        result += "Charge loss                = YES\n" if self.charge_loss else "Charge loss                = NO\n"
        result += "Recombination              = YES\n" if self.recombination else "Recombination              = NO\n"
        result += "*******************************************************\n"
        return result
    
    def replenish(self, charge, time) -> int:
        """
        Simulate charge replenishment for the pixel.

        Parameters:
            charge (float): Incoming charge
            time (float): Current time in nanoseconds.

        Returns:
            int: Instantaneous current based on replenishment.
        """
        if int(time) % CLOCK_FREQ == 0:
            #if we are at a tick of the clock cycle
            if self.active:
                # and if the pixel is active (ie the previous clock cycle did not contain a replenish event)
                if charge + self.charge >= self.reset * ELECTRON_CHARGE:
                    # if the charge in the capacitor is more than the threshold, execute replenish and return current
                    self.charge = float(Decimal(float(charge) + self.charge) - Decimal(self.reset * ELECTRON_CHARGE))
                    instantaneous_current = Decimal(self.reset * ELECTRON_CHARGE) / Decimal(time - self.prev_time)
                    self.prev_time = time
                    self.active = False
                    return instantaneous_current
                else:
                    # else just add the new charge
                    self.charge = float(charge) + self.charge
                    self.active = True
                    return 0
            else:
                # else just add the new charge
                self.charge = float(charge) + self.charge
                self.active = True
                return 0
        else:
            # else just add the new charge
            self.charge = float(charge) + self.charge
            return 0
