# Allan Online

**Allan Online** is an open source tool for simulating gyroscopes and accelerometers found on inertial measurement units (IMU). 
**Allan Online** gives users everywhere the power to characterize their navigation hardware in software!

The app is running on Heroku [here](http://allan-online.herokuapp.com/

# Current Features

- [x] Allan deviation plotting
- [x] Simulated, raw data plotting
- [x] Customizable noise parameters
    - [x] Angle random walk
    - [x] Bias instability
    - [x] Rate random walk

# Features TODO

*This is a list of patch level features to add in the future*

- [ ] Streaming data from hardware
- [ ] Calculate ADEV from file uploaded by user
- [ ] Interactive noise coefficient estimation
- [ ] Implement other common noise sources
    - [ ] Quantization noise
    - [ ] Rate Ramp
    - [ ] Sinusoidal
- [ ] Multiple, simultaneous simulations
- [ ] A "Demo" mode
