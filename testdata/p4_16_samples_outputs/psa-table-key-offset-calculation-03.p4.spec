
struct ethernet_t {
	bit<48> dstAddr
	bit<48> srcAddr
	bit<16> etherType
}

struct ipv4_t {
	bit<8> version_ihl
	bit<8> diffserv
	bit<32> totalLen
	bit<16> identification
	bit<16> flags_fragOffset
	bit<8> ttl
	bit<8> protocol
	bit<16> hdrChecksum
	bit<32> srcAddr
	bit<32> dstAddr
}

struct psa_ingress_output_metadata_t {
	bit<8> class_of_service
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
	bit<8> resubmit
	bit<32> multicast_group
	bit<32> egress_port
}

struct psa_egress_output_metadata_t {
	bit<8> clone
	bit<16> clone_session_id
	bit<8> drop
}

struct psa_egress_deparser_input_metadata_t {
	bit<32> egress_port
}

struct user_meta_t {
	bit<32> psa_ingress_input_metadata_ingress_port
	bit<8> psa_ingress_output_metadata_drop
	bit<32> psa_ingress_output_metadata_egress_port
	bit<48> MyIC_tbl_ethernet_srcAddr
	bit<8> MyIC_tbl_ipv4_protocol
	bit<32> MyIC_tbl_ipv4_dstAddr
	bit<32> MyIC_tbl_ipv4_srcAddr
	bit<48> MyIC_tbl_ethernet_dstAddr
}
metadata instanceof user_meta_t

header ethernet instanceof ethernet_t
header ipv4 instanceof ipv4_t

action NoAction args none {
	return
}

table tbl {
	key {
		m.MyIC_tbl_ethernet_srcAddr exact
		m.MyIC_tbl_ipv4_protocol exact
		m.MyIC_tbl_ipv4_dstAddr exact
		m.MyIC_tbl_ipv4_srcAddr exact
		m.MyIC_tbl_ethernet_dstAddr exact
	}
	actions {
		NoAction
	}
	default_action NoAction args none 
	size 0x10000
}


apply {
	rx m.psa_ingress_input_metadata_ingress_port
	mov m.psa_ingress_output_metadata_drop 0x0
	extract h.ethernet
	mov m.MyIC_tbl_ethernet_srcAddr h.ethernet.srcAddr
	mov m.MyIC_tbl_ipv4_protocol h.ipv4.protocol
	mov m.MyIC_tbl_ipv4_dstAddr h.ipv4.dstAddr
	mov m.MyIC_tbl_ipv4_srcAddr h.ipv4.srcAddr
	mov m.MyIC_tbl_ethernet_dstAddr h.ethernet.dstAddr
	table tbl
	jmpneq LABEL_DROP m.psa_ingress_output_metadata_drop 0x0
	tx m.psa_ingress_output_metadata_egress_port
	LABEL_DROP :	drop
}


