function g = grav_cylindre(x, rho, r, p_x, p_z)
    G=6.674e-8;
    g = ((2 * pi * G * rho * r^2) / p_z ) ./ (1 + (((p_x - x)./p_z).^2));
end
