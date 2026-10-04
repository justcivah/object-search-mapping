FROM osrf/ros:humble-desktop
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=1000
ARG RENDER_GID=992

RUN apt-get update && apt-get install -y --no-install-recommends \
        ros-humble-gazebo-ros-pkgs \
        ros-humble-ros-gz \
        python3-colcon-common-extensions \
        python3-vcstool \
        libgl1-mesa-dri mesa-vulkan-drivers \
        mesa-utils \
        sudo nano git \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid $USER_GID $USERNAME \
    && groupadd --gid $RENDER_GID render-host \
    && useradd --uid $USER_UID --gid $USER_GID -m -s /bin/bash $USERNAME \
    && usermod -aG video,render-host $USERNAME \
    && echo "$USERNAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USERNAME

USER $USERNAME
WORKDIR /home/$USERNAME/ros2_ws
RUN echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc \
    && echo "[ -f ~/ros2_ws/install/setup.bash ] && source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
