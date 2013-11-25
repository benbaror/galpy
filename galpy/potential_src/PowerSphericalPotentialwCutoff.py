###############################################################################
#   PowerSphericalPotentialwCutoff.py: spherical power-law potential w/ cutoff
#
#                                     amp
#                          rho(r)= ---------   e^{-(r/rc)^2}
#                                   r^\alpha
###############################################################################
import numpy as nu
from scipy import special, integrate
from Potential import Potential
class PowerSphericalPotentialwCutoff(Potential):
    """Class that implements spherical potentials that are derived from 
    power-law density models

                amp
    rho(r)= --------- e^{-(r/rc)^2}
             r^\alpha
    """
    def __init__(self,amp=1.,alpha=1.,rc=0.1,normalize=False):
        """
        NAME:
           __init__
        PURPOSE:
           initialize a power-law-density potential
        INPUT:
           amp - amplitude to be applied to the potential (default: 1)
           alpha - inner power
           rc - cut-off radius
           normalize - if True, normalize such that vc(1.,0.)=1., or, if 
                       given as a number, such that the force is this fraction 
                       of the force necessary to make vc(1.,0.)=1.
        OUTPUT:
           (none)
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        Potential.__init__(self,amp=amp)
        self.alpha= alpha
        self.rc= rc
        if normalize or isinstance(normalize,(int,float)):
            self.normalize(normalize)
        self.hasC= False

    def _evaluate(self,R,z,phi=0.,t=0.,dR=0,dphi=0):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
           dR, dphi - return dR, dphi-th derivative (only implemented for 0 and 1)
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2013-06-28 - Started - Bovy (IAS)
        """
        if dR == 0 and dphi == 0:
            r= nu.sqrt(R**2.+z**2.)
            return 2.*nu.pi*self.rc**(3.-self.alpha)/r*(r/self.rc*special.gamma(1.-self.alpha/2.)*special.gammainc(1.-self.alpha/2.,(r/self.rc)**2.)-special.gamma(1.5-self.alpha/2.)*special.gammainc(1.5-self.alpha/2.,(r/self.rc)**2.))
        elif dR == 1 and dphi == 0:
            return -self._Rforce(R,z,phi=phi,t=t)
        elif dR == 0 and dphi == 1:
            return -self._phiforce(R,z,phi=phi,t=t)

    def _Rforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2013-06-26 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R*R+z*z)
        return -self._mass(r)*R/r**3.

    def _zforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2013-06-26 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R*R+z*z)
        return -self._mass(r)*z/r**3.

    def _R2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rderiv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the second radial derivative
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R*R+z*z)
        return 4.*nu.pi*r**(-2.-self.alpha)*nu.exp(-(r/self.rc)**2.)*R**2.\
            +self._mass(r)/r**5.*(z**2.-2.*R**2.)

    def _z2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _z2deriv
        PURPOSE:
           evaluate the second vertical derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           the second vertical derivative
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R*R+z*z)
        return 4.*nu.pi*r**(-2.-self.alpha)*nu.exp(-(r/self.rc)**2.)*z**2.\
            +self._mass(r)/r**5.*(R**2.-2.*z**2.)

    def _Rzderiv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R*R+z*z)
        return R*z*(4.*nu.pi*r**(-2.-self.alpha)*nu.exp(-(r/self.rc)**2.)
                    -3.*self._mass(r)/r**5.)

    def _dens(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _dens
        PURPOSE:
           evaluate the density force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the density
        HISTORY:
           2013-06-28 - Written - Bovy (IAS)
        """
        r= nu.sqrt(R**2.+z**2.)
        return 1./r**self.alpha*nu.exp(-(r/self.rc)**2.)

    def _mass(self,r):
        """Helper function that has the mass"""
        return 2.*nu.pi*self.rc**(3.-self.alpha)*special.gammainc(1.5-self.alpha/2.,(r/self.rc)**2.)*special.gamma(1.5-self.alpha/2.)