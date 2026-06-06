"use client"

import { ReactNode } from "react";
import { Button } from "@heroui/button";
import { Modal, ModalContent, ModalHeader, ModalBody, ModalFooter } from "@heroui/modal";

interface IProps {
    isOpen: boolean;
    onClose: () => void;
    title: string;
    children: ReactNode;
    size?: "xs"|"sm"|"md"|"lg"|"xl";
}

const CustomModal = ({isOpen, onClose, title, children, size = "xs"}: IProps) => {
    return (
            <Modal isOpen={isOpen} onClose={onClose} size={size}>
                <ModalContent>
                    <ModalHeader className="border-b">
                        <h3 className="text-xl font-semibold">{title}</h3>
                    </ModalHeader>
                    <ModalBody className="space-y-4 py-6">
                        {children}
                    </ModalBody>
                </ModalContent>
            </Modal>
    );
}

export default CustomModal;
